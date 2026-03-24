# config.py
# ─────────────────────────────────────────────────────────────────
# Central place for all keywords and settings.
# ─────────────────────────────────────────────────────────────────

# Phrases used to find internship-related emails in Gmail.
# All multi-word so Gmail treats them as exact phrases (quoted).
APPLICATION_KEYWORDS = [
    "your application",
    "thank you for applying",
    "thank you for your application",
    "we received your application",
    "application received",
    "you have applied",
    "internship application",
    "summer 2026",
    "summer 2025",
    "new grad",
    "co-op",
    "coop",
    "application status",
    "application confirmation",
]

# Phrases that confirm an email is about YOUR application (not a newsletter).
# At least one of these must appear, or the email must come from a known platform.
CONFIRMATION_PHRASES = [
    "your application",
    "thank you for applying",
    "thank you for your application",
    "we received your application",
    "application received",
    "you have applied",
    "you applied",
    "we have received your",
    "your application has been",
    "applied for",
    "application for the",
    "application to",
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

# Keywords that indicate an ONLINE ASSESSMENT.
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

# Well-known job platform domains — emails from these are always real applications.
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
    "recruitcrm.io",
    "jobs.lever.co",
    "hire.com",
    "breezy.hr",
    "bamboohr.com",
    # OA platforms
    "hackerrank.com",
    "codility.com",
    "codesignal.com",
    "hirevue.com",
    "pymetrics.ai",
    "hiredscore.com",
    "karat.com",
]

# How far back to search (in days).
SEARCH_DAYS = 365
