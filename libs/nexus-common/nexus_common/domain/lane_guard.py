"""Detect when personal-lane content belongs in the business lane."""

import re

BUSINESS_INTENT_PATTERNS = [
    re.compile(p, re.I)
    for p in (
        r"\b(buy\s+now|shop\s+now|order\s+now|dm\s+to\s+(buy|order)|link\s+in\s+bio)\b",
        r"\b(for\s+sale|selling|on\s+sale|clearance|discount|%\s*off|promo\s*code)\b",
        r"\b(book\s+now|hire\s+me|my\s+services|our\s+services|get\s+a\s+quote)\b",
        r"\b(price|pricing|£\s*\d|€\s*\d|\$\s*\d|\d+\s*(gbp|usd|eur))\b",
        r"\b(marketplace|listing|checkout|add\s+to\s+cart)\b",
        r"\b(wholesale|retail|inventory|stock\s+left|limited\s+offer)\b",
        r"\b(freelance|consulting|agency|startup|side\s*hustle)\b",
        r"\b(commission|affiliate|sponsor\s+me|brand\s+deal)\b",
    )
]


def detect_business_intent(text: str) -> bool:
    """Return True when post text looks commercial and should live in business_general."""
    if not text or len(text.strip()) < 8:
        return False
    hits = sum(1 for pattern in BUSINESS_INTENT_PATTERNS if pattern.search(text))
    return hits >= 1


LANE_BUSINESS_DETAIL = (
    "This looks like business content. Switch to the Business lane and set up business tools "
    "to sell, promote, or advertise on NexSocio."
)