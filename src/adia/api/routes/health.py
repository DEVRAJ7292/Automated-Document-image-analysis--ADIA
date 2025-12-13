from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/", summary="Health check")
def health_check() -> dict:
    """
    Basic health check endpoint.

    Used by:
    - Docker
    - Kubernetes
    - Load balancers
    - Monitoring systems
    """
    return {
        "status": "ok",
        "service": "ADIA",
        "timestamp": datetime.utcnow().isoformat(),
    }
