from typing import Annotated

from fastapi import APIRouter, Depends
from nexus_common.domain.models import ApiResponse, HealthResponse

from services.professional.api.deps import get_professional_service, get_settings, get_token
from services.professional.application.dtos import (
    ProfessionalDashboardResponse,
    ProfessionalProfileResponse,
    UpdateProfessionalProfileRequest,
)
from services.professional.application.services import ProfessionalService
from services.professional.infrastructure.config import Settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    return HealthResponse(service=settings.service_name)


@router.get("/profile", response_model=ApiResponse[ProfessionalProfileResponse])
async def get_profile(
    token: Annotated[str, Depends(get_token)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[ProfessionalProfileResponse]:
    result = await service.get_profile(token)
    return ApiResponse(data=result)


@router.put("/profile", response_model=ApiResponse[ProfessionalProfileResponse])
async def update_profile(
    request: UpdateProfessionalProfileRequest,
    token: Annotated[str, Depends(get_token)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[ProfessionalProfileResponse]:
    result = await service.update_profile(token, request)
    return ApiResponse(data=result)


@router.get("/dashboard", response_model=ApiResponse[ProfessionalDashboardResponse])
async def dashboard(
    token: Annotated[str, Depends(get_token)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[ProfessionalDashboardResponse]:
    result = await service.get_dashboard(token)
    return ApiResponse(data=result)