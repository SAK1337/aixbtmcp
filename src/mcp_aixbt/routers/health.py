"""Health check endpoints for monitoring and orchestration."""

from datetime import datetime
from typing import Annotated, Any

import httpx
from fastapi import APIRouter, Depends

from mcp_aixbt import __version__
from mcp_aixbt.config import Settings, get_settings
from mcp_aixbt.models.responses import HealthStatus

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    """
    Basic health check endpoint.
    Returns healthy if the service is running.
    """
    return HealthStatus(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=__version__,
        checks={},
    )


@router.get("/health/ready", response_model=HealthStatus)
async def readiness_check(
    settings: Annotated[Settings, Depends(get_settings)]
) -> HealthStatus:
    """
    Readiness check - verifies the service can handle requests.
    Checks:
    - Configuration is valid
    - AIXBT API is reachable
    """
    checks: dict[str, Any] = {}
    overall_healthy = True

    # Check 1: Configuration
    try:
        _ = settings.aixbt_api_key.get_secret_value()
        checks["config"] = {"status": "pass", "message": "Configuration loaded"}
    except Exception as e:
        checks["config"] = {"status": "fail", "message": str(e)}
        overall_healthy = False

    # Check 2: AIXBT API connectivity
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://api.aixbt.tech/v2/projects/chains",
                headers={"x-api-key": settings.aixbt_api_key.get_secret_value()},
            )
            if response.status_code == 200:
                checks["aixbt_api"] = {"status": "pass", "message": "AIXBT API reachable"}
            else:
                checks["aixbt_api"] = {
                    "status": "warn",
                    "message": f"AIXBT API returned {response.status_code}",
                }
    except Exception as e:
        checks["aixbt_api"] = {"status": "fail", "message": str(e)}
        overall_healthy = False

    return HealthStatus(
        status="healthy" if overall_healthy else "unhealthy",
        timestamp=datetime.utcnow(),
        version=__version__,
        checks=checks,
    )


@router.get("/health/live")
async def liveness_check() -> dict[str, str]:
    """
    Liveness check - minimal check that service is running.
    Used by Kubernetes liveness probes.
    """
    return {"status": "alive"}
