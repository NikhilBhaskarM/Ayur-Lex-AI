import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_send_message_requires_auth(client: AsyncClient):
    response = await client.post("/api/v1/chat", json={
        "message": "Hello, can I patent this Ayurvedic formulation?"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_conversations_requires_auth(client: AsyncClient):
    response = await client.get("/api/v1/chat/conversations")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_list_conversations_empty(client: AsyncClient, auth_headers: dict):
    headers = {"Authorization": auth_headers["Authorization"]}
    response = await client.get("/api/v1/chat/conversations", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0
