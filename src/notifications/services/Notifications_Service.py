import httpx
from ..models.Notifications import NotificationBase, NotificationCreate, NotificationView
from ..db.Notifications_Repository import Notifications_Repository
from ..core import extensions as ext
from datetime import datetime
import uuid
from ..services.Email_Service import EmailService
from logging import getLogger

#qué hace el microservicio de verdad
logger = getLogger(__name__)

class Notifications_Service:
    def __init__(
        self,
        repository: Notifications_Repository | None = None,
        email_service: EmailService | None = None,
    ):
        self.repo = repository or Notifications_Repository(ext.db)
        self.email_service = email_service or EmailService()

#    def __init__(self, repository: Notifications_Repository | None = None):
 #       self.repo = repository or Notifications_Repository(ext.db)
        self.email_service = EmailService()

    async def register_event(
        self,
        data: NotificationCreate,
        user_email: str | None = None
    ) -> NotificationView:

        base = NotificationBase(**data.model_dump())
        notification = await self.repo.insert_notification(base)

        if user_email:
            logger.info(f"Enviando email a {user_email}")

            response = await self.email_service.send_notification_email(
                to_email=user_email,
                subject=data.title or "Nueva notificación",
                content=data.message,
            )

            logger.info(f"SendGrid response OK")

        return notification

    async def get_all(self) -> list[NotificationView]:
        return await self.repo.get_all_notifications()

    async def update(self, notification_id: str, data: dict):
        return await self.repo.update_notification(notification_id, data)

    async def delete(self, notification_id: str) -> bool:
        return await self.repo.delete_notification(notification_id)
    
#class UsersClient:
 #   async def get_user_email(self, user_id: str) -> str:
  #      # MOCK para desarrollo / swagger
   #     fake_users = {
   #         "123": "elenaberdu@gmail.com",
   #         "234": "bob@example.com",
   #         "1": "elenaberdu@gmail.com"
   #     }

        #return fake_users.get(user_id, "default@example.com")
    
class UsersClient:
    async def get_user_email(self, user_id: str) -> str | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://users-ms:8000/users/{user_id}")
            if resp.status_code == 200:
                return resp.json()["email"]
        return None


    



