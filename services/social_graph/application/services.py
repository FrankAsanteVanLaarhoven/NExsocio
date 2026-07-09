from uuid import UUID, uuid4

import httpx
from fastapi import HTTPException
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.social_graph.application.dtos import (
    ConnectionIdsResponse,
    ConnectionResponse,
    ConnectionsListResponse,
)
from services.social_graph.infrastructure.config import Settings
from services.social_graph.infrastructure.models import ConnectionModel


class SocialGraphService:
    def __init__(self, db: AsyncSession, settings: Settings):
        self.db = db
        self.settings = settings

    async def _fetch_display_name(self, user_id: UUID, token: str) -> str | None:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(
                    f"{self.settings.identity_service_url}/api/v1/users/{user_id}",
                    headers={"Authorization": f"Bearer {token}"},
                )
                if res.status_code == 200:
                    data = res.json().get("data", {})
                    return data.get("display_name")
        except httpx.HTTPError:
            return None
        return None

    async def request_connection(
        self, requester_id: UUID, recipient_id: UUID, token: str
    ) -> ConnectionResponse:
        if requester_id == recipient_id:
            raise HTTPException(status_code=400, detail="Cannot connect with yourself")

        existing = await self.db.execute(
            select(ConnectionModel).where(
                or_(
                    and_(
                        ConnectionModel.requester_id == requester_id,
                        ConnectionModel.recipient_id == recipient_id,
                    ),
                    and_(
                        ConnectionModel.requester_id == recipient_id,
                        ConnectionModel.recipient_id == requester_id,
                    ),
                )
            )
        )
        conn = existing.scalar_one_or_none()
        if conn:
            if conn.status == "accepted":
                raise HTTPException(status_code=409, detail="Already connected")
            if conn.status == "pending":
                raise HTTPException(status_code=409, detail="Connection request already pending")
            conn.status = "pending"
            conn.requester_id = requester_id
            conn.recipient_id = recipient_id
            await self.db.commit()
            await self.db.refresh(conn)
            return await self._to_response(conn, requester_id, token)

        connection = ConnectionModel(
            id=uuid4(),
            requester_id=requester_id,
            recipient_id=recipient_id,
            status="pending",
        )
        self.db.add(connection)
        await self.db.commit()
        await self.db.refresh(connection)
        return await self._to_response(connection, requester_id, token)

    async def accept_connection(self, user_id: UUID, connection_id: UUID, token: str) -> ConnectionResponse:
        result = await self.db.execute(
            select(ConnectionModel).where(ConnectionModel.id == connection_id)
        )
        conn = result.scalar_one_or_none()
        if not conn:
            raise HTTPException(status_code=404, detail="Connection not found")
        if conn.recipient_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to accept this request")
        if conn.status != "pending":
            raise HTTPException(status_code=400, detail="Connection is not pending")

        conn.status = "accepted"
        await self.db.commit()
        await self.db.refresh(conn)
        return await self._to_response(conn, user_id, token)

    async def list_connections(self, user_id: UUID, token: str) -> ConnectionsListResponse:
        result = await self.db.execute(
            select(ConnectionModel).where(
                or_(
                    ConnectionModel.requester_id == user_id,
                    ConnectionModel.recipient_id == user_id,
                )
            ).order_by(ConnectionModel.updated_at.desc())
        )
        all_conns = result.scalars().all()

        accepted: list[ConnectionResponse] = []
        pending_incoming: list[ConnectionResponse] = []

        for conn in all_conns:
            resp = await self._to_response(conn, user_id, token)
            if conn.status == "accepted":
                accepted.append(resp)
            elif conn.status == "pending" and conn.recipient_id == user_id:
                pending_incoming.append(resp)

        return ConnectionsListResponse(
            connections=accepted,
            pending_incoming=pending_incoming,
            total=len(accepted),
        )

    async def get_connection_ids(self, user_id: UUID) -> ConnectionIdsResponse:
        result = await self.db.execute(
            select(ConnectionModel).where(
                ConnectionModel.status == "accepted",
                or_(
                    ConnectionModel.requester_id == user_id,
                    ConnectionModel.recipient_id == user_id,
                ),
            )
        )
        conns = result.scalars().all()
        ids: list[UUID] = []
        for conn in conns:
            other = conn.recipient_id if conn.requester_id == user_id else conn.requester_id
            ids.append(other)
        ids.append(user_id)
        return ConnectionIdsResponse(user_ids=list(set(ids)))

    async def _to_response(
        self, conn: ConnectionModel, viewer_id: UUID, token: str
    ) -> ConnectionResponse:
        other_id = conn.recipient_id if conn.requester_id == viewer_id else conn.requester_id
        name = await self._fetch_display_name(other_id, token)
        return ConnectionResponse(
            id=conn.id,
            requester_id=conn.requester_id,
            recipient_id=conn.recipient_id,
            status=conn.status,
            created_at=conn.created_at,
            other_user_id=other_id,
            other_display_name=name,
        )