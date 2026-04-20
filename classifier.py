# classifier.py
# ─────────────────────────────────────────────────────────────────
# Classifies each email into a status category.
#
# CATEGORIES:
#   "oa"           — online assessment / coding challenge received
#   "rejected"     — company said no
#   "no_response"  — application confirmed, nothing back yet
#   (emails that don't look like real applications are dropped)
# ─────────────────────────────────────────────────────────────────

from config import REJECTED_KEYWORDS, OA_KEYWORDS, CONFIRMATION_PHRASES, PLATFORM_SENDERS,OFFER_KEYWORDS,INTERVIEW_KEYWORDS


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


def classify_email(email: dict) -> str:
    text = (email["subject"] + " " + email["snippet"] + " " + email["body"]).lower()

    if any(kw in text for kw in OA_KEYWORDS):
        return "oa"

    if any(kw in text for kw in REJECTED_KEYWORDS):
        return "rejected"

    return "no_response"


def classify_all(emails: list[dict]) -> list[dict]:
    results = []
    for email in emails:
        if not _is_real_application(email):
            continue                          # drop newsletters / notifications
        email["status"] = classify_email(email)
        results.append(email)
    return results


def classify_interview(email, all_emails_from_company):
    text = (email["subject"] + " " + email["snippet"] + " " + email["body"]).lower()

    if any(kw in text for kw in OFFER_KEYWORDS):
        return "offer"

    if any(kw in text for kw in INTERVIEW_KEYWORDS):
        #check if this is the first email from the company
        prior_interview = [e for e in all_emails_from_company if e["status"] in ["interview_1","interview_2","interview_3"]]

        #if this is the first email from the company it will be classified as interview_1
        if len(prior_interview) == 0:
            return "interview_1"
        else:
            return "interview_2"
