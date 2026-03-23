# classifier.py
# ─────────────────────────────────────────────────────────────────
# Classifies each email into a status category.
#
# CATEGORIES:
#   "rejected"     — company said no
#   "oa"           — online assessment / coding challenge received
#   "no_response"  — application confirmed but no further update
#   "other"        — caught by our query but doesn't fit above
#
# TODO: Implement classify_email() below.
# ─────────────────────────────────────────────────────────────────

from config import REJECTED_KEYWORDS, OA_KEYWORDS


def classify_email(email: dict) -> str:
  
    text = (email["subject"]+" "+ email["body"]).lower()
    if any(kw in text for kw in OA_KEYWORDS):             
          return "oa"

    if any(kw in text for kw in REJECTED_KEYWORDS):
          return "rejected"
    
    return "no_response"


def classify_all(emails: list[dict]) -> list[dict]:
    for email in emails:
         email["status"]= classify_email(email)
         
    return emails
