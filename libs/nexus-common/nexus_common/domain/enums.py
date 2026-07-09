from enum import StrEnum


class UserMode(StrEnum):
    """Age-adaptive and professional context modes."""

    KIDS = "kids"
    PRIME = "prime"
    PROFESSIONAL = "professional"


class VerificationStatus(StrEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"


class ContentVisibility(StrEnum):
    PUBLIC = "public"
    CONNECTIONS = "connections"
    PRIVATE = "private"


class ViewContext(StrEnum):
    PERSONAL = "personal"
    PROFESSIONAL = "professional"


class FeedType(StrEnum):
    GLOBAL = "global"
    CONNECTIONS = "connections"
    PROFESSIONAL = "professional"