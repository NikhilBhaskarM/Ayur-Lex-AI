import pytest
import pytest_asyncio
import asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.compiler import compiles

# Enable SQLite compilation for PostgreSQL UUID and JSONB types during tests
@compiles(UUID, "sqlite")
def compile_uuid_sqlite(type_, compiler, **kw):
    return "VARCHAR(36)"

@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

from app.main import create_app
from app.database import Base, get_db
import app.models  # Ensure all models are imported into Base.metadata

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def app(db_session):
    app_instance = create_app()

    async def override_get_db():
        yield db_session

    app_instance.dependency_overrides[get_db] = override_get_db
    yield app_instance
    app_instance.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def auth_headers(client, db_session):
    unique_email = f"auth_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "email": unique_email,
        "password": "SecurePassword123!",
        "full_name": "Test Practitioner"
    }
    await client.post("/api/v1/auth/register", json=user_data)
    response = await client.post("/api/v1/auth/login", json={
        "email": unique_email,
        "password": "SecurePassword123!"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}", "email": unique_email}
