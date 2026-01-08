import pytest
from src.notifications.app import create_app
import pytest_asyncio

from unittest.mock import patch
import pytest_asyncio
from src.notifications.app import create_app
from src.notifications.services.Notifications_Service import Notifications_Service
from unittest.mock import AsyncMock, patch

##### TEST IN-PROCESS

class RepoMemoryFake:
    def __init__(self):
        self.data = []

    async def insert_notification(self, notification):
        data = notification.model_dump()
        self.data.append(data)

        return {
            "ack": True,
            "id": "fake-id-123"
        }
    
class UsersClientFake:
    async def get_user_data(self, jwt, user_id):
        return {
            "email": "test@example.com",
            "plan": "pro",
            "name": "Usuario Test"
        }

@pytest.fixture
def app(monkeypatch):
    async def fake_init_db():
        return None

    monkeypatch.setattr("src.notifications.core.extensions.init_db_client", fake_init_db)

    app = create_app()
    return app

@pytest_asyncio.fixture
async def client():
    fake_repo = RepoMemoryFake()
    fake_users_client = UsersClientFake()

    def fake_init(self, repository=None, email_service=None, jwt=None):
        self.repo = fake_repo
        self.users_client = fake_users_client
        self.email_service = AsyncMock()  # evita SendGrid
        self.jwt = jwt

    with patch.object(Notifications_Service,"__init__", fake_init):
        app = create_app()

        async with app.test_app() as test_app:
            async with test_app.test_client() as client:
                yield client


# # ===========================================================
# # TEST 1: HEALTH
# # ===========================================================

@pytest.mark.asyncio
async def test_health_ok(client):
    res = await client.get("/v1/notifications/health")
    assert res.status_code == 200

    data = await res.get_json()
    assert data["status"] == "ok"


# # # ===========================================================
# # # TEST 2: LOGIN OK
# # # ===========================================================
# @pytest.mark.asyncio
# async def test_event_login_ok(client):
#     payload = {
#         "userId": "123",
#         "type": "login",
#         "metadata": {
#             "ip": "127.0.0.1",
#             "device": "Chrome"
#         }
#     }

#     res = await client.post(
#         "/v1/notifications/events",
#         json=payload
#     )

#     assert res.status_code == 201


# # ===========================================================
# # TEST 3: INVALID EVENT
# # ===========================================================
@pytest.mark.asyncio
async def test_event_invalid_type(client):
    payload = {
        "userId": "123",
        "type": "hackeo",
        "metadata": {}
    }

    res = await client.post(
        "/v1/notifications/events",
        json=payload,
        headers={
            "Authorization": "Bearer test.jwt.fake"
        }
    )

    assert res.status_code == 400

# # ===========================================================
# # TEST 13: MISSING EVENT
# # ===========================================================
@pytest.mark.asyncio
async def test_event_missing_userid(client):
    payload = {
        "type": "login",
        "metadata": {}
    }

    res = await client.post(
        "/v1/notifications/events",
        json=payload,
        headers={
            "Authorization": "Bearer test.jwt.fake"
        }
    )

    assert res.status_code == 400
