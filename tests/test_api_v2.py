import pytest
import httpx
from src.notifications.services.Notifications_Service import Notifications_Service

BASE_URL = "http://127.0.0.1:8000/v1/notifications"

##################
# 1. LOGIN OK
##################
@pytest.mark.asyncio
async def test_event_login_ok():
    payload = {
        "userId": "234",  # student
        "type": "login",
        "metadata": {
            "ip": "127.0.0.1",
            "device": "Chrome"
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/events", json=payload)

    assert res.status_code == 201
    data = res.json()

    assert data["type"] == "login"
    assert "inicio de sesión" in data["title"].lower()
    assert data["email_sent"] is True


##################
# 2. TIPO INVALIDO
##################
@pytest.mark.asyncio
async def test_event_invalid_type():
    payload = {
        "userId": "123",
        "type": "hackeo",
        "metadata": {}
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/events", json=payload)

    assert res.status_code == 400


##################
# 3. TRANSACCION OK
##################
@pytest.mark.asyncio
async def test_transaction_ok():
    payload = {
        "userId": "234",
        "type": "transaction-ok",
        "metadata": {
            "amount": 50,
            "currency": "EUR",
            "recipient": "Amazon"
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/events", json=payload)

    assert res.status_code == 201
    assert "pago realizado" in res.json()["title"].lower()


##################
# 4. TRANSACCION FALLIDA
##################
@pytest.mark.asyncio
async def test_transaction_failed():
    payload = {
        "userId": "234",
        "type": "transaction-failed",
        "metadata": {
            "reason": "Saldo insuficiente"
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/events", json=payload)

    assert res.status_code == 201
    assert "no se ha podido" in res.json()["title"].lower()


##################
# 5. HISTORY REQUEST - PRO OK
##################
@pytest.mark.asyncio
async def test_history_request_pro():
    payload = {
        "userId": "999",  # pro
        "type": "history-request",
        "metadata": {
            "month": "2025-01"
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/events", json=payload)

    assert res.status_code == 201
    assert "historial" in res.json()["title"].lower()
    assert res.json()["email_sent"] is True

##################
# 6. FRAUD DETECTED
##################
@pytest.mark.asyncio
async def test_fraud_detected():
    payload = {
        "userId": "234",
        "type": "fraud-detected",
        "metadata": {
            "reason": "Intentos sospechosos"
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/events", json=payload)

    assert res.status_code == 201
    assert "fraude" in res.json()["title"].lower()


##################
# 7. HEALTH
##################
@pytest.mark.asyncio
async def test_health():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/health")

    assert res.status_code == 200
    assert res.json()["status"] == "ok"


##################
# 8. OUT 
##################
def test_build_login_notification_in_process():
    service = Notifications_Service(...)
    title, message = service._build_login_message(
        ip="127.0.0.1",
        device="Chrome"
    )

    assert "inicio de sesión" in title.lower()
