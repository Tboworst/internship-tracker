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

