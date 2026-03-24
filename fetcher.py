import base64
import datetime
from config import APPLICATION_KEYWORDS, OA_KEYWORDS, PLATFORM_SENDERS, SEARCH_DAYS


def build_query() -> str:
    app_kw = " OR ".join(f'"{kw}"' if " " in kw else kw for kw in APPLICATION_KEYWORDS)
    oa_kw  = " OR ".join(f'"{kw}"' if " " in kw else kw for kw in OA_KEYWORDS)
    keyword_query = f"(subject:({app_kw}) OR ({oa_kw}))"

    since = datetime.date.today() - datetime.timedelta(days=SEARCH_DAYS)
    date_query = f"after:{since.strftime('%Y/%m/%d')}"

    return f"{keyword_query} {date_query}".strip()


def fetch_emails(service) -> list[dict]:
    query = build_query()
    emails = []
    page_token = None

    # Collect all message IDs across every page
    all_messages = []
    while True:
        kwargs = {"userId": "me", "q": query}
        if page_token:
            kwargs["pageToken"] = page_token

        response = service.users().messages().list(**kwargs).execute()
        all_messages.extend(response.get("messages", []))

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    # Fetch full message for each ID
    for msg_meta in all_messages:
        msg = service.users().messages().get(
            userId="me",
            id=msg_meta["id"],
            format="full"
        ).execute()

        headers = msg["payload"]["headers"]
        header_map = {h["name"]: h["value"] for h in headers}

        subject = header_map.get("Subject", "")
        sender  = header_map.get("From", "")
        date    = header_map.get("Date", "")
        body    = decode_body(msg["payload"])

        emails.append({
            "id":      msg_meta["id"],
            "subject": subject,
            "sender":  sender,
            "date":    date,
            "snippet": msg.get("snippet", ""),
            "body":    body
        })

    return emails


def decode_body(payload: dict) -> str:
    mime = payload.get("mimeType", "")

    if mime == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8")
        return ""

    if mime.startswith("multipart"):
        parts = payload.get("parts", [])
        return " ".join(decode_body(part) for part in parts)

    return ""
