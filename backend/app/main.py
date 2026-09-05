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

    return app


app = create_app()
