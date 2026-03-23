# main.py
# ─────────────────────────────────────────────────────────────────
# Entry point. Ties everything together and prints a summary report.
#
# Run with:  python main.py
# ─────────────────────────────────────────────────────────────────

from auth import get_gmail_service
from fetcher import fetch_emails
from classifier import classify_all
from collections import Counter


def print_report(emails: list[dict]):
    counts = Counter(email["status"] for email in emails)

    print("\n" + "─" * 35)
    print("  Internship Application Tracker")
    print("─" * 35)
    print(f"  Total emails found : {len(emails)}")
    print(f"  No response        : {counts.get('no_response', 0)}")
    print(f"  Rejected           : {counts.get('rejected', 0)}")
    print(f"  Online Assessments : {counts.get('oa', 0)}")
    print("─" * 35)

    for status, label in [("oa", "Online Assessments"), ("rejected", "Rejected")]:
        group = [e for e in emails if e["status"] == status]
        if group:
            print(f"\n{label}:")
            for e in group:
                print(f"  • {e['subject']} — {e['sender']}")


def main():
    print("Connecting to Gmail...")

    service = get_gmail_service()
    print("Fetching emails (this may take a moment)...")
    # TODO: call fetch_emails(service) and store the result
    emails = fetch_emails(service)  # replace with fetch_emails(service)

    print(f"Found {len(emails)} relevant emails.")

    classified = classify_all(emails)
  # print out the reports 
    print_report(classified)


if __name__ == "__main__":
    main()
