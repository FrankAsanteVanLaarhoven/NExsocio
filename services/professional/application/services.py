from uuid import UUID

import httpx
from fastapi import HTTPException

from services.professional.application.dtos import (
    NetworkInsight,
    ProfessionalDashboardResponse,
    ProfessionalProfileResponse,
    UpdateProfessionalProfileRequest,
)
from services.professional.infrastructure.config import Settings


class ProfessionalService:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def _identity_request(self, method: str, path: str, token: str, json: dict | None = None):
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.request(
                method,
                f"{self.settings.identity_service_url}{path}",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json=json,
            )
            if res.status_code >= 400:
                detail = res.json().get("detail", res.text) if res.text else "Identity service error"
                raise HTTPException(status_code=res.status_code, detail=detail)
            return res.json().get("data")

    async def get_profile(self, token: str) -> ProfessionalProfileResponse:
        data = await self._identity_request("GET", "/api/v1/users/me", token)
        return ProfessionalProfileResponse(
            user_id=UUID(data["id"]),
            display_name=data["display_name"],
            headline=data.get("headline"),
            company=data.get("company"),
            skills=data.get("skills"),
            bio=data.get("bio"),
        )

    async def update_profile(
        self, token: str, request: UpdateProfessionalProfileRequest
    ) -> ProfessionalProfileResponse:
        payload = request.model_dump(exclude_none=True)
        data = await self._identity_request("PUT", "/api/v1/users/me", token, payload)
        return ProfessionalProfileResponse(
            user_id=UUID(data["id"]),
            display_name=data["display_name"],
            headline=data.get("headline"),
            company=data.get("company"),
            skills=data.get("skills"),
            bio=data.get("bio"),
        )

    async def get_dashboard(self, token: str) -> ProfessionalDashboardResponse:
        profile = await self.get_profile(token)
        return ProfessionalDashboardResponse(
            profile=profile,
            insights=[
                NetworkInsight(label="Profile Views", value="128", trend="up"),
                NetworkInsight(label="Connection Growth", value="+12%", trend="up"),
                NetworkInsight(label="Engagement", value="4.2%", trend="neutral"),
            ],
            connection_suggestions=[
                "Engineers in your network",
                "Product leaders nearby",
                "Robotics integrators",
            ],
        )