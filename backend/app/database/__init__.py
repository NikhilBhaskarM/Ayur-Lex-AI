"""Database session management and base model."""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.compiler import compiles
import structlog

from app.config import settings

logger = structlog.get_logger(__name__)

# Compile rules for SQLite compatibility during local development without PostgreSQL
@compiles(UUID, "sqlite")
def compile_uuid_sqlite(type_, compiler, **kw):
    return "VARCHAR(36)"

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

import os

db_url = settings.DATABASE_URL
engine_kwargs = {"echo": settings.is_development}

try:
    if "sqlite" not in db_url:
        engine_kwargs.update({"pool_pre_ping": True, "pool_size": 10, "max_overflow": 20})
    engine = create_async_engine(db_url, **engine_kwargs)
except Exception:
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ayurveda_ipr.db")).replace("\\", "/")
    sqlite_url = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(sqlite_url, echo=False)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
async_session_maker = async_session_factory


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


async def get_db() -> AsyncSession:
    """Dependency that provides a database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables with automatic local SQLite fallback if PostgreSQL is not running."""
    global engine, async_session_factory, async_session_maker
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized on primary database")
    except Exception as e:
        logger.warning(
            "Primary database connection failed. Falling back to local SQLite database (ayurveda_ipr.db)",
            error=str(e)
        )
        import os
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ayurveda_ipr.db")).replace("\\", "/")
        sqlite_url = f"sqlite+aiosqlite:///{db_path}"
        engine = create_async_engine(sqlite_url, echo=False)
        async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async_session_maker = async_session_factory
        logger.info("Local SQLite database initialized successfully (ayurveda_ipr.db)")

    # Ensure default admin accounts exist
    try:
        from app.models.user import User
        from app.core.security import hash_password
        from sqlalchemy import select
        import uuid

        admin_pwd_hash = hash_password("Admin@123")
        async with async_session_factory() as session:
            for admin_email, admin_name, admin_id in [
                ("researcher@ayurlex.ai", "Ayur-Lex Researcher", "00000000-0000-0000-0000-000000000001"),
                ("admin@ayurlex.ai", "System Administrator", "00000000-0000-0000-0000-000000000002")
            ]:
                res = await session.execute(select(User).filter(User.email == admin_email))
                user = res.scalars().first()
                if not user:
                    user = User(
                        id=uuid.UUID(admin_id),
                        email=admin_email,
                        password_hash=admin_pwd_hash,
                        full_name=admin_name,
                        role="ADMIN",
                        preferred_language="en",
                        is_active=True
                    )
                    session.add(user)
                elif user.password_hash == "demo_hash":
                    user.password_hash = admin_pwd_hash
            await session.commit()
    except Exception as e:
        logger.warning("Admin seeding skipped or error", error=str(e))
