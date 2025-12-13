from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adia.core.config import get_settings
from adia.core.logging import setup_logging
from adia.api.routes.health import router as health_router
from adia.api.routes.upload import router as upload_router
from adia.api.routes.query import router as query_router


def create_app() -> FastAPI:
    """
    Application factory.

    This pattern allows:
    - Testing without side effects
    - Multiple deployments (API, worker, etc.)
    """

    settings = get_settings()

    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        debug=settings.DEBUG,
    )

    # ─────────────────────────────
    # Middleware
    # ─────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ─────────────────────────────
    # Routes
    # ─────────────────────────────
    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(upload_router, tags=["Documents"])
    app.include_router(query_router, tags=["Query"])



    return app


app = create_app()
