# DeerFlow-X Backend Tests
# This file contains basic smoke tests for the API endpoints.

import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test the /health endpoint returns 200."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert data["service"] == "deer-flow-x"


@pytest.mark.asyncio
async def test_create_task(client):
    """Test POST /tasks creates a task and returns queued status."""
    response = await client.post("/tasks", json={"task": "test task"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert "task_id" in data


@pytest.mark.asyncio
async def test_get_task(client):
    """Test GET /tasks/{task_id} returns task info."""
    # First create a task
    create_resp = await client.post("/tasks", json={"task": "find me"})
    task_id = create_resp.json()["task_id"]

    # Then retrieve it
    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] in ("queued", "pending")
