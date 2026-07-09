from uuid import UUID

from pydantic import BaseModel, Field


class ProfessionalProfileResponse(BaseModel):
    user_id: UUID
    display_name: str
    headline: str | None = None
    company: str | None = None
    skills: str | None = None
    bio: str | None = None


class UpdateProfessionalProfileRequest(BaseModel):
    headline: str | None = Field(default=None, max_length=128)
    company: str | None = Field(default=None, max_length=128)
    skills: str | None = Field(default=None, max_length=500)
    bio: str | None = Field(default=None, max_length=500)


class NetworkInsight(BaseModel):
    label: str
    value: str
    trend: str = "neutral"


class ProfessionalDashboardResponse(BaseModel):
    profile: ProfessionalProfileResponse
    insights: list[NetworkInsight]
    connection_suggestions: list[str]