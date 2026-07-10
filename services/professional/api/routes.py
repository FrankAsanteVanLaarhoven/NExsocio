from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from nexus_common.domain.models import ApiResponse, HealthResponse

from services.professional.api.deps import (
    AuthContext,
    get_auth_context,
    get_compliance_service,
    get_professional_service,
    get_settings,
    get_token,
)
from services.professional.application.corporate_compliance import CorporateComplianceService
from services.professional.application.dtos import (
    BusinessProfileResponse,
    CorporateComplianceStatus,
    CorporateCredentialResponse,
    CorporateDashboardResponse,
    CorporateServiceListingResponse,
    CreateCorporateServiceRequest,
    CreateOrganizationRequest,
    OrganizationResponse,
    OrgMembershipResponse,
    OrgNetworkingAccess,
    ProfessionalDashboardResponse,
    ProfessionalProfileResponse,
    SubmitCorporateCredentialsRequest,
    UpdateProfessionalProfileRequest,
    UpsertBusinessProfileRequest,
    VerifyCorporateEmailRequest,
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


@router.get("/dashboard/corporate", response_model=ApiResponse[CorporateDashboardResponse])
async def corporate_dashboard(
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    token: Annotated[str, Depends(get_token)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[CorporateDashboardResponse]:
    result = await service.get_corporate_dashboard(token, auth.user_id)
    return ApiResponse(data=result)


@router.get("/business-profile", response_model=ApiResponse[BusinessProfileResponse | None])
async def get_business_profile(
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[BusinessProfileResponse | None]:
    result = await service.get_business_profile(auth.user_id)
    return ApiResponse(data=result)


@router.put("/business-profile", response_model=ApiResponse[BusinessProfileResponse])
async def upsert_business_profile(
    request: UpsertBusinessProfileRequest,
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[BusinessProfileResponse]:
    result = await service.upsert_business_profile(auth.user_id, request)
    return ApiResponse(data=result)


@router.get("/organizations", response_model=ApiResponse[list[OrganizationResponse]])
async def list_organizations(
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
    industry: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    public_only: bool = Query(default=False),
) -> ApiResponse[list[OrganizationResponse]]:
    result = await service.list_organizations(industry=industry, sector=sector, public_only=public_only)
    return ApiResponse(data=result)


@router.get("/corporate/sectors", response_model=ApiResponse[list[dict]])
async def corporate_sectors(
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
) -> ApiResponse[list[dict]]:
    return ApiResponse(data=compliance.list_sectors())


@router.get("/corporate/services/public", response_model=ApiResponse[list[CorporateServiceListingResponse]])
async def public_corporate_services(
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
    sector: str | None = Query(default=None),
) -> ApiResponse[list[CorporateServiceListingResponse]]:
    return ApiResponse(data=await compliance.list_public_services(sector=sector))


@router.get(
    "/organizations/{org_id}/compliance",
    response_model=ApiResponse[CorporateComplianceStatus],
)
async def org_compliance(
    org_id: UUID,
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
) -> ApiResponse[CorporateComplianceStatus]:
    return ApiResponse(data=await compliance.get_compliance(org_id))


@router.post(
    "/organizations/{org_id}/verify-email",
    response_model=ApiResponse[CorporateComplianceStatus],
)
async def verify_org_email(
    org_id: UUID,
    request: VerifyCorporateEmailRequest,
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
) -> ApiResponse[CorporateComplianceStatus]:
    return ApiResponse(data=await compliance.verify_email(org_id, auth.email, request))


@router.post(
    "/organizations/{org_id}/credentials",
    response_model=ApiResponse[CorporateCredentialResponse],
)
async def submit_org_credentials(
    org_id: UUID,
    request: SubmitCorporateCredentialsRequest,
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
) -> ApiResponse[CorporateCredentialResponse]:
    if not await service.user_belongs_to_org(auth.user_id, org_id):
        raise HTTPException(status_code=403, detail="Must be an organisation member")
    return ApiResponse(data=await compliance.submit_credentials(org_id, request))


@router.post(
    "/organizations/{org_id}/subscription/trial",
    response_model=ApiResponse[OrgNetworkingAccess],
)
async def start_networking_trial(
    org_id: UUID,
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
) -> ApiResponse[OrgNetworkingAccess]:
    if not await service.user_belongs_to_org(auth.user_id, org_id):
        raise HTTPException(status_code=403, detail="Must be an organisation member")
    return ApiResponse(data=await compliance.start_networking_trial(org_id))


@router.get(
    "/organizations/{org_id}/networking",
    response_model=ApiResponse[OrgNetworkingAccess],
)
async def org_networking_access(
    org_id: UUID,
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
) -> ApiResponse[OrgNetworkingAccess]:
    return ApiResponse(data=await compliance.networking_access(org_id))


@router.post(
    "/organizations/{org_id}/services",
    response_model=ApiResponse[CorporateServiceListingResponse],
)
async def create_corporate_service(
    org_id: UUID,
    request: CreateCorporateServiceRequest,
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
) -> ApiResponse[CorporateServiceListingResponse]:
    if not await service.user_belongs_to_org(auth.user_id, org_id):
        raise HTTPException(status_code=403, detail="Must be an organisation member")
    result = await compliance.create_public_service(
        org_id, request.title, request.description, request.price_hint
    )
    return ApiResponse(data=result)


@router.get(
    "/organizations/{org_id}/can-sell",
    response_model=ApiResponse[bool],
)
async def org_can_sell(
    org_id: UUID,
    compliance: Annotated[CorporateComplianceService, Depends(get_compliance_service)],
) -> ApiResponse[bool]:
    return ApiResponse(data=await compliance.can_serve_public(org_id))


@router.post("/organizations", response_model=ApiResponse[OrganizationResponse])
async def create_organization(
    request: CreateOrganizationRequest,
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[OrganizationResponse]:
    result = await service.create_organization(auth.user_id, request)
    return ApiResponse(data=result)


@router.get("/organizations/memberships", response_model=ApiResponse[list[OrgMembershipResponse]])
async def list_memberships(
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[list[OrgMembershipResponse]]:
    result = await service.list_memberships(auth.user_id)
    return ApiResponse(data=result)


@router.get("/organizations/{org_id}/membership-check", response_model=ApiResponse[bool])
async def membership_check(
    org_id: UUID,
    auth: Annotated[AuthContext, Depends(get_auth_context)],
    service: Annotated[ProfessionalService, Depends(get_professional_service)],
) -> ApiResponse[bool]:
    result = await service.user_belongs_to_org(auth.user_id, org_id)
    return ApiResponse(data=result)