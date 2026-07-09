from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from nexus_common.domain.models import ApiResponse, HealthResponse

from services.social_graph.api.deps import (
    get_current_user_id,
    get_settings,
    get_social_service,
    get_token,
)
from services.social_graph.application.dtos import (
    ConnectionIdsResponse,
    ConnectionRequest,
    ConnectionResponse,
    ConnectionsListResponse,
)
from services.social_graph.application.services import SocialGraphService
from services.social_graph.infrastructure.config import Settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    return HealthResponse(service=settings.service_name)


@router.post("/connections", response_model=ApiResponse[ConnectionResponse])
async def request_connection(
    request: ConnectionRequest,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    token: Annotated[str, Depends(get_token)],
    service: Annotated[SocialGraphService, Depends(get_social_service)],
) -> ApiResponse[ConnectionResponse]:
    result = await service.request_connection(user_id, request.recipient_id, token)
    return ApiResponse(data=result)


@router.post("/connections/{connection_id}/accept", response_model=ApiResponse[ConnectionResponse])
async def accept_connection(
    connection_id: UUID,
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    token: Annotated[str, Depends(get_token)],
    service: Annotated[SocialGraphService, Depends(get_social_service)],
) -> ApiResponse[ConnectionResponse]:
    result = await service.accept_connection(user_id, connection_id, token)
    return ApiResponse(data=result)


@router.get("/connections", response_model=ApiResponse[ConnectionsListResponse])
async def list_connections(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    token: Annotated[str, Depends(get_token)],
    service: Annotated[SocialGraphService, Depends(get_social_service)],
) -> ApiResponse[ConnectionsListResponse]:
    result = await service.list_connections(user_id, token)
    return ApiResponse(data=result)


@router.get("/connections/ids", response_model=ApiResponse[ConnectionIdsResponse])
async def connection_ids(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    service: Annotated[SocialGraphService, Depends(get_social_service)],
) -> ApiResponse[ConnectionIdsResponse]:
    result = await service.get_connection_ids(user_id)
    return ApiResponse(data=result)