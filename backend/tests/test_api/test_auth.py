import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "full_name": "Dr. Charaka",
        "password": "StrongPassword123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert data["full_name"] == "Dr. Charaka"

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    # Register first time
    await client.post("/api/v1/auth/register", json={
        "email": "dup@example.com",
        "full_name": "Dr. Sushruta",
        "password": "StrongPassword123!"
    })
    
    # Register second time
    response = await client.post("/api/v1/auth/register", json={
        "email": "dup@example.com",
        "full_name": "Dr. Sushruta",
        "password": "StrongPassword123!"
    })
    assert response.status_code in (400, 422)
    assert "already registered" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    # Register user
    await client.post("/api/v1/auth/register", json={
        "email": "loginuser@example.com",
        "full_name": "Vaidya Sharma",
        "password": "StrongPassword123!"
    })
    
    # Login with JSON payload
    response = await client.post("/api/v1/auth/login", json={
        "email": "loginuser@example.com",
        "password": "StrongPassword123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    # Register user
    await client.post("/api/v1/auth/register", json={
        "email": "wrongpass@example.com",
        "full_name": "Vaidya Verma",
        "password": "StrongPassword123!"
    })
    
    # Login with wrong password
    response = await client.post("/api/v1/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "WrongPassword123!"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "email": "ghost@example.com",
        "password": "StrongPassword123!"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_me_authenticated(client: AsyncClient, auth_headers: dict):
    headers = {"Authorization": auth_headers["Authorization"]}
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == auth_headers["email"]

@pytest.mark.asyncio
async def test_get_me_unauthenticated(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "weak@example.com",
        "full_name": "Weak Pass User",
        "password": "123"
    })
    assert response.status_code in (400, 422)
