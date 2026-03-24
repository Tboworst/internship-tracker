# api.py
# ─────────────────────────────────────────────────────────────────
# FastAPI backend — handles Gmail OAuth and serves email data.
#
# Run locally:  uvicorn api:app --reload
# ─────────────────────────────────────────────────────────────────

import base64
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from auth import create_web_oauth_flow, get_gmail_service
from fetcher import fetch_emails
from classifier import classify_all

app = FastAPI()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
SECRET_KEY = os.environ["SECRET_KEY"]          # set in Railway env vars
ADMIN_KEY  = os.getenv("ADMIN_KEY", "")        # set in Railway — only you know this
OAUTH_STATES: dict[str, str] = {}              # state -> code_verifier
user_count: int = 0                            # resets on redeploy

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ── Auth helpers ───────────────────────────────────────────────────

def _make_session_token(access_token: str, refresh_token: str) -> str:
    """Creates a signed JWT containing the user's Gmail tokens."""
    payload = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def _get_service_from_header(authorization: str | None):
    """Validates the Bearer JWT and returns a Gmail service object."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated. Please sign in.")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please sign in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token.")
    return get_gmail_service(payload["access_token"], payload["refresh_token"])


# ── OAuth routes ───────────────────────────────────────────────────

@app.get("/auth/google/start")
def auth_google_start():
    """Redirects the user to Google's OAuth consent screen."""
    state = secrets.token_urlsafe(24)

    # Generate PKCE pair so we can verify it in the callback
    code_verifier = secrets.token_urlsafe(96)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode()

    flow = create_web_oauth_flow(state=state)
    auth_url, returned_state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    OAUTH_STATES[returned_state] = code_verifier
    return RedirectResponse(auth_url)


@app.get("/auth/google/callback")
def auth_google_callback(
    state: str = Query(...),
    code: str = Query(None),
    error: str = Query(None),
):
    """Handles the redirect back from Google, issues a session JWT."""
    if error:
        return RedirectResponse(f"{FRONTEND_URL}/?auth=error&reason={error}")

    if state not in OAUTH_STATES:
        return RedirectResponse(f"{FRONTEND_URL}/?auth=error&reason=invalid_state")

    code_verifier = OAUTH_STATES.pop(state)
    flow = create_web_oauth_flow(state=state)
    flow.fetch_token(code=code, code_verifier=code_verifier)

    creds = flow.credentials
    session_token = _make_session_token(creds.token, creds.refresh_token)

    global user_count
    user_count += 1

    return RedirectResponse(f"{FRONTEND_URL}/?token={session_token}")


@app.get("/auth/status")
def auth_status(authorization: str | None = Header(None)):
    """Returns whether the current request has a valid session."""
    if not authorization or not authorization.startswith("Bearer "):
        return {"authenticated": False}
    token = authorization.split(" ", 1)[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"authenticated": True}
    except Exception:
        return {"authenticated": False}


# ── Data routes ────────────────────────────────────────────────────

@app.get("/emails")
def get_emails(authorization: str | None = Header(None)):
    """Fetches, classifies, and returns the user's internship emails."""
    try:
        service = _get_service_from_header(authorization)
        emails = fetch_emails(service)
        classified = classify_all(emails)
        return classified
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/summary")
def get_summary(authorization: str | None = Header(None)):
    """Returns counts per status."""
    return get_emails(authorization)


# ── Admin route (only you) ─────────────────────────────────────────

@app.get("/admin/stats")
def admin_stats(key: str = Query(default="")):
    """Returns user count. Protected by ADMIN_KEY query param."""
    if not ADMIN_KEY or key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"users_since_last_deploy": user_count}
