import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    # It might FAIL during local test if Redis/DB aren't reachable from host
    # But checking status code is 200 is good enough for connectivity
    assert response.status_code == 200
    data = response.json()
    assert "overall" in data
    assert "api" in data
    assert data["api"] == "PASS"


@pytest.mark.asyncio
async def test_read_events(client: AsyncClient):
    response = await client.get("/api/events", follow_redirects=True)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Length depends on DB state, but structure should match


@pytest.mark.asyncio
async def test_read_calendar(client: AsyncClient):
    response = await client.get("/calendar/ctf.ics", follow_redirects=True)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/calendar")
    assert "BEGIN:VCALENDAR" in response.text
