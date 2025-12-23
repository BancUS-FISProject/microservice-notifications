from ..models.Notifications import NotificationBase, NotificationCreate, NotificationView
from ..db.Notifications_Repository import Notifications_Repository
from ..core import extensions as ext
from datetime import datetime
import uuid

#qué hace el microservicio de verdad

class Notifications_Service:
    def __init__(self, repository: Notifications_Repository | None = None):
        self.repo = repository or Notifications_Repository(ext.db)

    async def register_event(self, data: NotificationCreate) -> NotificationView:
        # Creamos el objeto base con createdAt
        base = NotificationBase(**data.model_dump())


        return await self.repo.insert_notification(base)
    
    async def get_all(self) -> list[NotificationView]:
        return await self.repo.get_all_notifications()

    #async def get_notifications_for_user(self, user_id: str) -> list[NotificationView]:
     #   return await self.repo.find_notifications_by_user(user_id)

from ..services.Email_Service import EmailService

class Notifications_Service:
    def __init__(self, repository=None):
        self.repo = repository or Notifications_Repository(ext.db)
        self.email_service = EmailService()

    async def register_event(
        self,
        data: NotificationCreate,
        user_email: str | None = None
    ) -> NotificationView:

        base = NotificationBase(**data.model_dump())
        notification = await self.repo.insert_notification(base)

        # Enviar email si tenemos correo
        if user_email:
            await self.email_service.send_notification_email(
                to_email=user_email,
                subject=data.title or "Nueva notificación",
                content=data.message
            )

        return notification

