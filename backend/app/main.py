"""
Ayurvedic IPR & Regulatory AI Assistant — FastAPI Application Factory

Main entry point for the backend application.
"""

import logging
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db


def configure_logging():
    """Configure structured logging."""
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if settings.is_development
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    log = structlog.get_logger()
    log.info("Starting application", app_name=settings.APP_NAME, env=settings.APP_ENV)

    # Initialize database tables (development convenience)
    if settings.is_development:
        try:
            await init_db()
            log.info("Database tables created/verified")
        except Exception as e:
            log.error("Failed to initialize database tables", error=str(e))

    yield

    log.info("Shutting down application")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        description=(
            "AI-powered assistant for Ayurvedic intellectual property, "
            "traditional knowledge, biodiversity compliance, and regulatory guidance. "
            "All responses are citation-grounded and jurisdiction-aware."
        ),
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    from fastapi.responses import RedirectResponse
    @app.get("/api/docs", include_in_schema=False)
    async def docs_redirect():
        return RedirectResponse(url="/docs")


    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes
    from app.api.router import api_router
    app.include_router(api_router, prefix="/api/v1")

    # Modular Extension Routers (Features 1, 3, 6)
    from app.api.triage import router as triage_router
    app.include_router(triage_router, prefix="/api/triage", tags=["triage"])
    app.include_router(triage_router, prefix="/api/v1/triage", tags=["triage"])

    from app.api.abs_compliance import router as compliance_router
    app.include_router(compliance_router, prefix="/api/compliance", tags=["compliance"])
    app.include_router(compliance_router, prefix="/api/v1/compliance", tags=["compliance"])

    from app.api.synergy import router as synergy_router
    app.include_router(synergy_router, prefix="/api/analytics", tags=["synergy"])
    app.include_router(synergy_router, prefix="/api/v1/analytics", tags=["synergy"])
    app.include_router(synergy_router, prefix="/api/fer", tags=["fer"])
    app.include_router(synergy_router, prefix="/api/v1/fer", tags=["fer"])

    # Direct mount for debate WebSocket streaming
    from app.api.v1.debate_stream import router as debate_router
    app.include_router(debate_router, prefix="/api/v1/ws", tags=["debate"])
    app.include_router(debate_router, prefix="/ws", tags=["debate"])

    # DPDP Act 2023 Compliance Middleware
    from app.middleware.sanitizer import DPDPSanitizerMiddleware
    app.add_middleware(DPDPSanitizerMiddleware)

    # -----------------------------------------------------------------
    # Frontend Static Asset Mounting & SPA Client Routing (Option A)
    # Strictly mounted AFTER all /api, /ws, and OpenAPI route definitions
    # -----------------------------------------------------------------
    import os
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    from fastapi import HTTPException

    # Resolve repo root and frontend/dist
    backend_app_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(backend_app_dir))
    dist_path = os.path.join(repo_root, "frontend", "dist")

    if os.path.isdir(dist_path):
        assets_dir = os.path.join(dist_path, "assets")
        if os.path.isdir(assets_dir):
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        locales_dir = os.path.join(dist_path, "locales")
        if os.path.isdir(locales_dir):
            app.mount("/locales", StaticFiles(directory=locales_dir), name="locales")

        @app.get("/", include_in_schema=False)
        async def serve_root():
            index_path = os.path.join(dist_path, "index.html")
            if os.path.isfile(index_path):
                return FileResponse(index_path)
            raise HTTPException(status_code=404, detail="Frontend index.html not found")

        @app.get("/{full_path:path}", include_in_schema=False)
        async def serve_spa_catchall(full_path: str):
            # Do not intercept unmatched API, WebSocket, or docs routes
            if full_path.startswith("api/") or full_path.startswith("ws/") or full_path in ("docs", "redoc", "openapi.json"):
                raise HTTPException(status_code=404, detail="Route not found")

            # Serve matching static file in frontend/dist if present (e.g., favicon, vite.svg)
            target_path = os.path.join(dist_path, full_path)
            if full_path and os.path.isfile(target_path):
                return FileResponse(target_path)

            # Fallback to index.html for client-side routing
            index_path = os.path.join(dist_path, "index.html")
            if os.path.isfile(index_path):
                return FileResponse(index_path)
            raise HTTPException(status_code=404, detail="Frontend index.html not found")

    return app


app = create_app()
