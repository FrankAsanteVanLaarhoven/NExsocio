from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from nexus_common.domain.enums import UserMode


@dataclass
class User:
    id: UUID
    email: str
    display_name: str
    password_hash: str
    mode: UserMode
    age_verified: bool
    zkp_proof_hash: str | None
    created_at: datetime
    updated_at: datetime