# auth.py
# ─────────────────────────────────────────────────────────────────
# Handles Gmail OAuth2 authentication.
#
# SETUP INSTRUCTIONS:
#   1. Go to https://console.cloud.google.com/
#   2. Create a new project (e.g. "internship-tracker")
#   3. Go to "APIs & Services" → "Enable APIs"
#      Search for and enable "Gmail API"
#   4. Go to "APIs & Services" → "Credentials"
#      Click "Create Credentials" → "OAuth client ID"
#      Choose "Desktop app", give it a name, click Create
#   5. Download the JSON file and save it as credentials.json
#      in this project folder
#   6. Run this script once — a browser window will open asking
#      you to log in and grant access. After that, token.json
#      is saved and you won't need to log in again.
# ─────────────────────────────────────────────────────────────────

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# We only need read access to your mailbox.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


def get_gmail_service():
    """
    Authenticates with Gmail and returns a service object.

    TODO: Call this function from fetcher.py to get the `service`
    you'll use for all Gmail API calls.
    """
    creds = None

    # Load saved token if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, start the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next time
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service
