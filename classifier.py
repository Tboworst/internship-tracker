# classifier.py
# ─────────────────────────────────────────────────────────────────
# Classifies each email into a status category.
#
# CATEGORIES:
#   "offer"        — company extended an offer
#   "interview_1"  — first interview (behavioral or unknown type)
#   "interview_2"  — follow-up interview from the same company
#   "oa"           — online assessment / coding challenge received
#   "rejected"     — company said no
#   "no_response"  — application confirmed, nothing back yet
#   (emails that don't look like real applications are dropped)
# ─────────────────────────────────────────────────────────────────

import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from config import (
    REJECTED_KEYWORDS,
    OA_KEYWORDS,
    INTERVIEW_KEYWORDS,
    OFFER_KEYWORDS,
    CONFIRMATION_PHRASES,
    PLATFORM_SENDERS,
)


def _is_real_application(email: dict) -> bool:
    """
    Returns True only if the email looks like it's about an actual
    application — either sent from a known hiring platform, or
    containing standard application confirmation language.
    """
    sender = email.get("sender", "").lower()
    if any(platform in sender for platform in PLATFORM_SENDERS):
        return True

    text = (email["subject"] + " " + email["snippet"] + " " + email["body"]).lower()
    return any(phrase in text for phrase in CONFIRMATION_PHRASES)


def _extract_domain(sender: str) -> str:
    """Pulls the domain out of a sender string like 'Name <email@company.com>'."""
    match = re.search(r"@([\w.-]+)", sender)
    return match.group(1).lower() if match else ""


def _parse_date(email: dict) -> datetime:
    """Parse the email date for sorting. Falls back to epoch on failure."""
    try:
        return parsedate_to_datetime(email.get("date", ""))
    except Exception:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def classify_email(email: dict, company_interview_counts: dict) -> str:
    """
    Returns a status string for a single email.

    `company_interview_counts` is a shared dict (mutated here) that tracks
    how many interview emails we've already seen per company domain —
    so we can tell interview_1 apart from interview_2.
    """
    text = (email["subject"] + " " + email["snippet"] + " " + email["body"]).lower()

    # Offers first — most specific signal
    if any(kw in text for kw in OFFER_KEYWORDS):
        return "offer"

    # Interview — use domain to decide if this is a 1st or 2nd round
    if any(kw in text for kw in INTERVIEW_KEYWORDS):
        domain = _extract_domain(email.get("sender", ""))
        count = company_interview_counts.get(domain, 0)
        company_interview_counts[domain] = count + 1
        return "interview_1" if count == 0 else "interview_2"

    if any(kw in text for kw in OA_KEYWORDS):
        return "oa"

    if any(kw in text for kw in REJECTED_KEYWORDS):
        return "rejected"

    return "no_response"


def classify_all(emails: list[dict]) -> list[dict]:
    # Sort oldest-first so interview sequences are detected in the right order
    sorted_emails = sorted(emails, key=_parse_date)

    # Tracks how many interview emails we've seen per company domain
    company_interview_counts: dict[str, int] = {}

    results = []
    for email in sorted_emails:
        if not _is_real_application(email):
            continue                          # drop newsletters / notifications
        email["status"] = classify_email(email, company_interview_counts)
        results.append(email)

    return results
