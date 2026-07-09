from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.professional.application.services import ProfessionalService
from services.professional.infrastructure.config import Settings

settings = Settings()
security = HTTPBearer()


def get_settings() -> Settings:
    return settings


async def get_professional_service(
    cfg: Annotated[Settings, Depends(get_settings)],
) -> ProfessionalService:
    return ProfessionalService(cfg)


async def get_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    return credentials.credentials