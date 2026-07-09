from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ConnectionRequest(BaseModel):
    recipient_id: UUID


class ConnectionResponse(BaseModel):
    id: UUID
    requester_id: UUID
    recipient_id: UUID
    status: str
    created_at: datetime
    other_user_id: UUID
    other_display_name: str | None = None


class ConnectionsListResponse(BaseModel):
    connections: list[ConnectionResponse]
    pending_incoming: list[ConnectionResponse]
    total: int


class ConnectionIdsResponse(BaseModel):
    user_ids: list[UUID]