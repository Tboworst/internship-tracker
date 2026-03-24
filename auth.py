# auth.py
# ─────────────────────────────────────────────────────────────────
# Web OAuth2 flow for Gmail.
#
# Set these environment variables in Railway:
#   GOOGLE_CLIENT_ID     — from Google Cloud Console → Credentials
#   GOOGLE_CLIENT_SECRET — from Google Cloud Console → Credentials
#   REDIRECT_URI         — your Railway URL + /auth/google/callback
#                          e.g. https://your-app.up.railway.app/auth/google/callback
# ─────────────────────────────────────────────────────────────────

import os
from typing import Optional
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _client_config() -> dict:
    """Builds the OAuth client config from environment variables."""
    redirect_uri = os.environ["REDIRECT_URI"]
    return {
        "web": {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri],
        }
    }


def create_web_oauth_flow(state: Optional[str] = None) -> Flow:
    """Creates a Google OAuth web flow using env var credentials."""
    flow = Flow.from_client_config(_client_config(), scopes=SCOPES, state=state)
    flow.redirect_uri = os.environ["REDIRECT_URI"]
    return flow


def get_gmail_service(access_token: str, refresh_token: str):
    """Builds a Gmail service object from a user's stored OAuth tokens."""
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)
