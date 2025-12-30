import pytest
import httpx
from src.notifications.core import extensions as ext

BASE_URL = "http://127.0.0.1:8000/v1/notifications/"

##################
# TEST LOGIN
##################
@pytest.mark.asyncio
async def test_event_login():
    payload = {
        "userId": "123",
        "type": "login",
        "metadata": {}
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(
            "http://127.0.0.1:8000/v1/notifications/events",
            json=payload
        )

    print(f"\n[test_event_login] Status: {res.status_code}")
    print(f"[test_event_login] Response: {res.text}")
    
    assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
    data = res.json()
    print(f"[test_event_login] JSON: {data}")
    assert data["type"] == "login"
    assert "inicio de sesión" in data["message"].lower()

##################
# TEST TYPE INVALIDO
##################

@pytest.mark.asyncio
async def test_event_invalid_type():
    payload = {
        "userId": "123",
        "type": "hackeo",
        "metadata": {}
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(
            "http://127.0.0.1:8000/v1/notifications/events",
            json=payload
        )

    assert res.status_code == 400

##################
# TEST HISTORY-REQUEST
##################

@pytest.mark.asyncio
async def test_event_history():
    payload = {
        "userId": "123",
        "type": "history-request",
        "metadata": {
            "from": "2025-01-01",
            "to": "2025-01-31",
            "transactions": [
                {"date": "2025-01-02", "amount": -50, "description": "Supermercado"}
            ]
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(
            "http://127.0.0.1:8000/v1/notifications/events",
            json=payload
        )

    print(f"\n[test_event_history] Status: {res.status_code}")
    print(f"[test_event_history] Response: {res.text}")
    
    assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
    data = res.json()
    print(f"[test_event_history] JSON: {data}")
    assert "historial" in data["title"].lower()
