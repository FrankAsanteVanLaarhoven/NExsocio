"""Corporate sector taxonomy and email rules for NexSocio B2B lane."""

from typing import TypedDict

# Personal email providers — blocked for corporate org registration
FREE_EMAIL_DOMAINS = frozenset({
    "gmail.com", "googlemail.com", "yahoo.com", "hotmail.com", "outlook.com",
    "live.com", "icloud.com", "me.com", "aol.com", "proton.me", "protonmail.com",
    "mail.com", "gmx.com", "yandex.com", "zoho.com",
})

CORPORATE_TRIAL_DAYS = 30
CORPORATE_NETWORKING_MONTHLY_GBP = 49.0


class CorporateSector(TypedDict):
    id: str
    label: str
    description: str
    examples: str


CORPORATE_SECTORS: list[CorporateSector] = [
    {"id": "healthcare", "label": "Health & Care", "description": "Hospitals, clinics, care homes, telehealth", "examples": "NHS partners, home care, mental health"},
    {"id": "wellbeing", "label": "Wellbeing", "description": "Wellness, therapy, coaching, mindfulness", "examples": "Counselling, fitness coaching, EAP"},
    {"id": "legal", "label": "Legal", "description": "Law firms, solicitors, barristers, compliance", "examples": "Corporate law, family law, immigration"},
    {"id": "accounting", "label": "Accounting & Finance", "description": "Accountants, auditors, bookkeepers, CFO services", "examples": "Tax, payroll, audit, advisory"},
    {"id": "education", "label": "Education", "description": "Schools, universities, training, e-learning", "examples": "Courses, apprenticeships, professional certs"},
    {"id": "sports", "label": "Sports & Recreation", "description": "Clubs, leagues, facilities, sports medicine", "examples": "Gyms, academies, event management"},
    {"id": "faith", "label": "Faith & Community", "description": "Churches, mosques, temples, community groups", "examples": "Online church, charity, fellowship"},
    {"id": "technology", "label": "Technology", "description": "Software, IT services, SaaS, consulting", "examples": "Dev shops, MSPs, product companies"},
    {"id": "nonprofit", "label": "Non-profit & NGO", "description": "Charities, foundations, social enterprises", "examples": "Fundraising, volunteering, advocacy"},
    {"id": "professional_services", "label": "Professional Services", "description": "Consulting, agencies, B2B services", "examples": "Marketing, HR, design, engineering"},
    {"id": "general", "label": "General Corporate", "description": "Other verified organisations", "examples": "Any qualifying company"},
]

SECTOR_IDS = frozenset(s["id"] for s in CORPORATE_SECTORS)


def extract_email_domain(email: str) -> str:
    return email.strip().lower().split("@")[-1]


def is_corporate_email(email: str) -> bool:
    domain = extract_email_domain(email)
    return bool(domain) and domain not in FREE_EMAIL_DOMAINS and "." in domain


def email_domain_matches(email: str, expected_domain: str) -> bool:
    return extract_email_domain(email) == expected_domain.strip().lower()