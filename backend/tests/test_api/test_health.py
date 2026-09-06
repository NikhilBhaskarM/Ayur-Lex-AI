import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_endpoint_returns_200(client: AsyncClient):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_health_response_structure(client: AsyncClient):
    response = await client.get("/api/v1/health")
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    # May include version, environment, or database connectivity depending on implementation
