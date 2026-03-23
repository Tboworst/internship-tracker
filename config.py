# config.py
# ─────────────────────────────────────────────────────────────────
# Central place for all keywords and settings.
# Tweak these lists to match the emails you're actually receiving.
# ─────────────────────────────────────────────────────────────────

# Keywords that suggest an email is about an internship application.
# Used to find relevant emails in your inbox/sent folder.
APPLICATION_KEYWORDS = [
    "internship",
    "intern",
    "application",
    "applied",
    "your application",
    "thank you for applying",
    "summer 2026",
    "new grad",
    "co-op",
    "coop",
]

# Keywords that indicate a REJECTION.
REJECTED_KEYWORDS = [
    "unfortunately",
    "we regret",
    "not moving forward",
    "not selected",
    "other candidates",
    "position has been filled",
    "will not be moving",
    "decided to move forward with other",
    "no longer considering",
    "we have decided",
]

# Keywords that indicate an ONLINE ASSESSMENT
OA_KEYWORDS = [
    "online assessment",
    "coding assessment",
    "technical assessment",
    "hackerrank",
    "codility",
    "hirevue",
    "pymetrics",
    "codesignal",
    "assessment invitation",
    "take-home",
]

# Well-known job platform domains used to confirm you applied.
PLATFORM_SENDERS = [
    "greenhouse.io",
    "lever.co",
    "workday.com",
    "myworkdayjobs.com",
    "taleo.net",
    "icims.com",
    "smartrecruiters.com",
    "ashbyhq.com",
    "linkedin.com",
    "jobvite.com",
]

# How far back to search (in days). Set to None to search all mail.
SEARCH_DAYS = 365
