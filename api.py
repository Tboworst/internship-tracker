# api.py
# ─────────────────────────────────────────────────────────────────
# FastAPI backend — wraps your existing Python script as an API
# so the React frontend can request your email data over HTTP.
#
# Run with:  uvicorn api:app --reload
# Then visit: http://localhost:8000/emails
# ─────────────────────────────────────────────────────────────────

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import get_gmail_service
from fetcher import fetch_emails
from classifier import classify_all

app = FastAPI()

# CORS lets your React app (running on port 5173) talk to this API.
# Without this, the browser blocks cross-origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/emails")
def get_emails():
    """
    Fetches, classifies, and returns all internship emails as JSON.

    The React frontend will call this endpoint on page load.
    Returns a list of email objects, each with a "status" field.
    """
    try:
        service = get_gmail_service()
        emails = fetch_emails(service)
        classified = classify_all(emails)
        return classified
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/summary")
def get_summary():
    """
    Returns just the counts per status — useful for the summary cards.

    TODO (optional): call get_emails() logic and return counts like:
      { "total": 47, "no_response": 28, "rejected": 14, "oa": 5 }
    """
    try:
        summary = get_emails()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
