from fastapi import APIRouter
from nexus_common.domain.models import ApiResponse, HealthResponse
from pydantic import BaseModel
from services._template_stub import create_stub_app

app = create_stub_app(
    "robot-agent",
    "Robot & embodied agent integration layer (architectural stub)",
    8006,
)

router = APIRouter(prefix="/api/v1")


class DigitalTwin(BaseModel):
    agent_id: str
    name: str
    status: str = "online"
    safety_channel: str = "certified_stub_v1"


class RobotPresence(BaseModel):
    agent_id: str
    social_status: str = "available"


@router.get("/twins", response_model=ApiResponse[list[DigitalTwin]])
async def list_twins() -> ApiResponse[list[DigitalTwin]]:
    return ApiResponse(
        data=[
            DigitalTwin(agent_id="twin-001", name="Nexus Explorer", status="standby"),
            DigitalTwin(agent_id="twin-002", name="Safety Monitor", status="online"),
        ]
    )


@router.post("/commands/stub", response_model=ApiResponse[dict])
async def stub_command(agent_id: str, command: str) -> ApiResponse[dict]:
    return ApiResponse(
        data={
            "agent_id": agent_id,
            "command": command,
            "status": "accepted",
            "safety_check": "passed_stub",
        }
    )


app.include_router(router)