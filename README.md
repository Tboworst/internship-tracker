# Internship Application Tracker

Scans your Gmail and categorizes internship emails into:
- **No response** — application confirmed, nothing since
- **Rejected** — company sent a rejection
- **OA** — online assessment / coding challenge received

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get Gmail credentials (one-time)
#    Follow the instructions at the top of auth.py
#    Place credentials.json in this folder

# 3. Run the script
python main.py
```

---

## File Guide

| File | What to implement |
|------|-------------------|
| `config.py` | Tweak keywords and sender lists to match your emails |
| `auth.py` | Already complete — just add credentials.json |
| `fetcher.py` | `build_query()`, `fetch_emails()`, `decode_body()` |
| `classifier.py` | `classify_email()`, `classify_all()` |
| `main.py` | Wire everything together in `main()`, format `print_report()` |

---

## Suggested Implementation Order

1. **`config.py`** — read through and customize the keyword lists
2. **`auth.py`** — follow the Google Cloud setup steps, run `python auth.py` to confirm it connects
3. **`fetcher.py`** — implement `build_query()` first, test it in the Gmail search bar, then implement `fetch_emails()` and `decode_body()`
4. **`classifier.py`** — implement `classify_email()` with keyword checks, test it on a few sample email strings
5. **`main.py`** — plug the functions together and implement `print_report()`
