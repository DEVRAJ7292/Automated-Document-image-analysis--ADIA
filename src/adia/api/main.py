from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

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
    # API Routes
    # ─────────────────────────────
    app.include_router(health_router, prefix="/health", tags=["Health"])
    app.include_router(upload_router, tags=["Documents"])
    app.include_router(query_router, tags=["Query"])

    # ─────────────────────────────
    # UI (Serve index.html at /)
    # ─────────────────────────────
    ui_dir = Path("ui")

    if ui_dir.exists():
        # Serve static assets if any (css/js/images)
        app.mount("/static", StaticFiles(directory=ui_dir), name="static")

        @app.get("/", include_in_schema=False)
        def serve_ui():
            return FileResponse(ui_dir / "index.html")

    return app


app = create_app()
