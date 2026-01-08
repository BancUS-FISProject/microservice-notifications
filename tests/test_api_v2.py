import pytest
import contextlib
from unittest.mock import AsyncMock, patch

import httpx

# Import REAL del servicio pasando repo en memoria
from src.notifications.services.Notifications_Service import Notifications_Service
from src.notifications.db.Notifications_Repository import Notifications_Repository


BASE_URL = "http://127.0.0.1:8000/v1/notifications"


# ===========================================================
# REPO FAKE EN MEMORIA
# ===========================================================
class RepoMemoryFake:
    """Simula MongoRepository para tests unitarios"""
    def __init__(self):
        self.data = []

    async def insert_notification(self, notification: dict):
        self.data.append(notification)
        return {"ack": True}

    async def get_notifications_by_user(self, iban: str):
        return [n for n in self.data if n.get("user") == iban]

    async def get_all_notifications(self):
        return self.data
    
    async def fetch_history_from_transactions(self, user_id: str, mode: str):
        return {
            "transactions": [
                {"date":"2026-01-07T12:00:00.000Z",
                 "amount":100,
                 "currency":"EUR",
                 "description":"mock"}
            ]
        }

    async def delete_notification(self, _id: str):
        raise RuntimeError("Simulated Mongo failure")

    async def update_notification_title(self, _id: str, title: str):
        raise RuntimeError("Simulated Mongo failure")


# ===========================================================
# FIXTURE CON MOCK EXTERNO
# ===========================================================
@pytest.fixture
def service_unitario():
    fake_repo = RepoMemoryFake()

    # parchear constructor para que NO use ext.db
    with patch.object(Notifications_Repository, "__init__", return_value=None):
        # inyectar JWT skip y usuarios
        svc = Notifications_Service(repository=fake_repo)
        yield svc


# ===========================================================
# TEST 1: LOGIN OK
# ===========================================================
@pytest.mark.asyncio
async def test_event_login_ok(service_unitario):
    payload = {
        "userId": "123",
        "type": "login",
        "metadata": {
            "ip": "127.0.0.1",
            "device": "Chrome"
        }
    }

    res = await httpx.AsyncClient().post(
        f"{BASE_URL}/events",
        json=payload,
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"}
    )

    # este endpoint NO protegido → 201
    assert res.status_code == 201


# ===========================================================
# TEST 2: TIPO INVALIDO
# ===========================================================
@pytest.mark.asyncio
async def test_event_invalid_type(service_unitario):
    payload = {
        "userId": "123",
        "type": "invalido",
        "metadata": {}
    }

    res = await httpx.AsyncClient().post(
        f"{BASE_URL}/events",
        json=payload,
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"}
    )

    assert res.status_code == 400


# ===========================================================
# TEST 3: TRANSFER OK
# ===========================================================
@pytest.mark.asyncio
async def test_transaction_ok(service_unitario):
    payload = {
        "userId": "123",
        "type": "transaction",
        "metadata": {
            "amount": 50,
            "recipient": "Casero Piso Triana"
        }
    }

    res = await httpx.AsyncClient().post(
        f"{BASE_URL}/events",
        json=payload,
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"}
    )

    assert res.status_code == 201

# ===========================================================
# TEST 4: TRANSFER NEGATIVE OK
# ===========================================================
@pytest.mark.asyncio
async def test_transaction_negative_ok(service_unitario):
    payload = {
        "userId": "123",
        "type": "transaction",
        "metadata": {
            "amount": -75,
            "recipient": "gym"
        }
    }

    res = await httpx.AsyncClient().post(
        f"{BASE_URL}/events",
        json=payload,
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"}
    )

    assert res.status_code == 201


# ===========================================================
# TEST 5: FRAUD
# ===========================================================
@pytest.mark.asyncio
async def test_fraud_detected(service_unitario):
    payload = {
        "userId": "123",
        "type": "fraud-detected",
        "metadata": {
            "reason": "test fraude detectado",
            "account": "FRAUD12345"
        }
    }

    res = await httpx.AsyncClient().post(
        f"{BASE_URL}/events",
        json=payload,
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"}
    )

    assert res.status_code == 201

# ===========================================================
# TEST 6: UPDATE FAIL
# ===========================================================
@pytest.mark.asyncio
async def test_update_notification_title_returns_error(service_unitario):

    res = await httpx.AsyncClient().put(
        f"{BASE_URL}/1",
        json={"title": "updated title"}
    )

    assert res.status_code in (404, 500)


# ===========================================================
# TEST 7: DELETE NON EXISTING
# ===========================================================
@pytest.mark.asyncio
async def test_delete_non_existing_notification(service_unitario):

    res = await httpx.AsyncClient().delete(
        f"{BASE_URL}/000000000000000000000000"
    )

    assert res.status_code in (404, 500)

# ===========================================================
# TEST 8: SEND EMAIL SENDGRID
# ===========================================================
@pytest.mark.asyncio
async def test_send_email_sendgrid():

    res = await httpx.AsyncClient().post(
        f"{BASE_URL}/test-email"
    )

# ==========================================================
# TEST 9: HEALTH
# ==========================================================
@pytest.mark.asyncio
async def test_health():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/health")

    assert res.status_code == 200
    assert res.json()["status"] == "ok"


# # ===========================================================
# # TEST 9: UPDATE y DELETE REALES
# # ===========================================================
# @pytest.mark.asyncio
# async def test_update_and_delete_real_flow(service_unitario):

#     # 1. Crear notificación
#     async with httpx.AsyncClient() as client:
#         res_create = await client.post(
#             f"{BASE_URL}/events",
#             json={"userId":"123",
#                   "type":"login",
#                   "metadata":{}},
#             headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"}
#         )

#     created = res_create.json()
#     notification_id = created.get("id")
    
#     # DEPURACIÓN
#     print("CREATED OBJECT >>>", created)
#     print("TYPE >>>", type(created))
#     print("EXTRACTED _id >>>", notification_id)

#     # 2. Update
#     async with httpx.AsyncClient() as client:
#         res_up = await client.put(
#             f"{BASE_URL}/{notification_id}",
#             json={"title":"nuevo"}
#         )

#     assert res_up.status_code in (200,404)

#     # 3. Delete
#     async with httpx.AsyncClient() as client:
#         res_del = await client.delete(
#             f"{BASE_URL}/{notification_id}"
#         )

#     assert res_del.status_code in (200,404)


