import httpx
from ..models.Notifications import NotificationBase, NotificationCreate, NotificationView, NotificationEvent
from ..db.Notifications_Repository import Notifications_Repository
from ..core import extensions as ext
from datetime import datetime
import uuid
from ..services.Email_Service import EmailService
from logging import getLogger
import ssl
import certifi

#qué hace el microservicio de verdad
logger = getLogger(__name__)
# FIX SSL 
ssl_context = ssl.create_default_context(cafile=certifi.where())

class Notifications_Service:
    def __init__(
        self,
        repository: Notifications_Repository | None = None,
        email_service: EmailService | None = None,
    ):
        self.repo = repository or Notifications_Repository(ext.db)
        self.email_service = email_service or EmailService()


class Notifications_Service:

    def __init__(
        self,
        repository: Notifications_Repository | None = None,
        email_service: EmailService | None = None,
        #users_client: UsersClient | None = None,
    ):
        self.repo = repository or Notifications_Repository(ext.db)
        self.email_service = email_service or EmailService()
        self.users_client = UsersClient()

    async def handle_event(self, event: NotificationEvent) -> NotificationView:
        """
        Punto único de entrada para eventos desde otros microservicios.
        Construye la notificación, la guarda y envía el email al usuario.
        """

        metadata = event.metadata or {}

        # ======================
        # LOGIN
        # ======================
        if event.type == "login":
            timestamp = metadata.get("timestamp", "fecha desconocida")
            device = metadata.get("device", "dispositivo desconocido")
            ip = metadata.get("ip", "IP desconocida")

            title = "Nuevo inicio de sesión en tu cuenta"
            message = (
                f"Hemos detectado un inicio de sesión en tu cuenta.\n\n"
                f"Fecha y hora: {timestamp}\n"
                f"Dispositivo: {device}\n"
                f"Dirección IP: {ip}\n\n"
                f"Si no has sido tú, te recomendamos cambiar tu contraseña "
                f"y contactar con nuestro servicio de atención al cliente."
            )

        # ======================
        # TRANSACCIÓN OK
        # ======================
        elif event.type == "transaction-ok":
            amount = metadata.get("amount", "importe desconocido")
            currency = metadata.get("currency", "EUR")
            recipient = metadata.get("recipient", "destinatario desconocido")
            timestamp = metadata.get("timestamp", "fecha desconocida")

            title = "Pago realizado correctamente"
            message = (
                f"Tu operación se ha completado con éxito.\n\n"
                f"Importe: {amount} {currency}\n"
                f"Destinatario: {recipient}\n"
                f"Fecha: {timestamp}\n\n"
                f"Puedes consultar el detalle completo desde tu área personal."
            )

        # ======================
        # TRANSACCIÓN FALLIDA
        # ======================
        elif event.type == "transaction-failed":
            amount = metadata.get("amount", "importe desconocido")
            currency = metadata.get("currency", "EUR")
            recipient = metadata.get("recipient", "destinatario desconocido")
            reason = metadata.get("reason", "motivo no especificado")
            timestamp = metadata.get("timestamp", "fecha desconocida")

            title = "No se ha podido completar tu pago"
            message = (
                f"Hemos intentado realizar una operación, pero no ha sido posible.\n\n"
                f"Importe: {amount} {currency}\n"
                f"Destinatario: {recipient}\n"
                f"Fecha: {timestamp}\n"
                f"Motivo: {reason}\n\n"
                f"Por favor, revisa tus datos o inténtalo de nuevo más tarde."
            )
        
        # ----------------------
        # PAGO PROGRAMADO
        # ----------------------
        elif event.type == "scheduled-payment":
            amount = event.metadata.get("amount")
            date = event.metadata.get("scheduledDate")
            recipient = event.metadata.get("recipient")

            title = "Pago programado"
            message = (
                f"Se ha programado un nuevo pago en tu cuenta.\n\n"
                f"• Destinatario: {recipient}\n"
                f"• Importe: {amount}\n"
                f"• Fecha de ejecución: {date}"
            )

        # ======================
        # HISTORIAL
        # ======================
        elif event.type == "history-request":
            title = "Tu historial de movimientos"
            message = self.format_history_email(event.metadata)

        else:
            raise ValueError(f"Tipo de evento no soportado: {event.type}")

        
        # Obtener email del usuario
        email = await self.users_client.get_user_email(event.userId)

        # Crear notificación
        notification = NotificationCreate(
            userId=event.userId,
            type=event.type,
            title=title,
            message=message,
            metadata=event.metadata,
            email=email,
        )

        # Guardar en Mongo
        saved = await self.repo.insert_notification(
            NotificationBase(**notification.model_dump())
        )

        # Enviar email si existe
        if email:
            logger.info(f"Enviando email a {email}")
            await self.email_service.send_notification_email(
                to_email=email,
                subject=title,
                content=message,
            )

        return saved
    

    def format_history_email(self, metadata: dict) -> str:
        transactions = metadata.get("transactions", [])
        from_date = metadata.get("from", "—")
        to_date = metadata.get("to", "—")
        numRecords = len(transactions)

        if not transactions:
            return (
                f"Has solicitado tu historial de movimientos "
                f"del {from_date} al {to_date}, pero no se han encontrado operaciones."
            )

        lines = [
            f"Historial de movimientos del {from_date} al {to_date}:",
            ""
        ]

        for tx in transactions:
            amount = tx.get("amount", 0)
            sign = "+" if amount > 0 else ""
            lines.append(
                f"• {tx.get('date')} | {sign}{amount} € | {tx.get('description')}"
            )

        lines.append("")
        lines.append("Si no reconoces alguna operación, contacta con tu entidad bancaria.")

        return "\n".join(lines)
    

    async def get_all(self) -> list[NotificationView]:
        return await self.repo.get_all_notifications()


    async def update(self, notification_id: str, data: dict):
        return await self.repo.update_notification(notification_id, data)


    async def delete(self, notification_id: str) -> bool:
        return await self.repo.delete_notification(notification_id)
    


class UsersClient:
    async def get_user_email(self, user_id: str) -> str:
        # MOCK para desarrollo / swagger
        fake_users = {
            "123": "elenaberdu@gmail.com",
            "234": "bob@example.com",
            "1": "elenaberdu@gmail.com"
        }

        return fake_users.get(user_id, "default@example.com")
    


class UsersClientsss:
    async def get_user_email(self, user_id: str) -> str | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://users-ms:8000/users/{user_id}")
            if resp.status_code == 200:
                return resp.json()["email"]
        return "No se ha encontrado el usuario"


    



