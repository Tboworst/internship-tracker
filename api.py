# api.py
# ─────────────────────────────────────────────────────────────────
# FastAPI backend — handles Gmail OAuth and serves email data.
#
# Run locally:  uvicorn api:app --reload
# ─────────────────────────────────────────────────────────────────

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
OAUTH_STATES: set[str] = set()

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
    flow = create_web_oauth_flow(state=state)
    auth_url, returned_state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    OAUTH_STATES.add(returned_state)
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

    OAUTH_STATES.discard(state)
    flow = create_web_oauth_flow(state=state)
    flow.fetch_token(code=code)

    creds = flow.credentials
    session_token = _make_session_token(creds.token, creds.refresh_token)

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
