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

---

## Deploy + OAuth (Railway + Vercel)

You need both deployment **and** Google OAuth app setup.

### 1) Deploy first

- Backend (FastAPI) on Railway, e.g. `https://your-backend.up.railway.app`
- Frontend (React) on Vercel, e.g. `https://your-frontend.vercel.app`

### 2) Configure backend environment variables (Railway)

- `FRONTEND_URL=https://your-frontend.vercel.app`
- `GOOGLE_CLIENT_ID=` (from Google Cloud Console)
- `GOOGLE_CLIENT_SECRET=` (from Google Cloud Console)
- `REDIRECT_URI=https://your-backend.up.railway.app/auth/google/callback`
- `SECRET_KEY=` (any long random string — run `python -c "import secrets; print(secrets.token_hex(32))"`)

### 3) Configure frontend environment variables (Vercel)

- `VITE_API_URL=https://your-backend.up.railway.app`

### 4) Google Cloud OAuth setup

In **Google Cloud Console** -> APIs & Services -> Credentials -> your OAuth client:

- **Authorized redirect URI**:
  - `https://your-backend.up.railway.app/auth/google/callback`
- **Authorized JavaScript origins** (if prompted):
  - `https://your-frontend.vercel.app`
  - `https://your-backend.up.railway.app`

In **OAuth consent screen**:

- **App home page**: your frontend URL, e.g. `https://your-frontend.vercel.app`
- **Privacy policy**: a public URL you host (can be a simple page in frontend)
- **Terms of service**: optional, but recommended public URL

### 5) Where to get homepage/privacy URLs

- **Homepage URL**: your deployed frontend domain on Vercel.
- **Privacy policy URL**: use:
  `https://your-frontend.vercel.app/privacy.html`
- **Terms URL**: use:
  `https://your-frontend.vercel.app/terms.html`

If you do not have privacy/terms pages yet, create simple placeholder pages first, deploy, then paste those URLs in Google Console.
