from email.mime import message
from importlib.metadata import metadata
from turtle import mode
import httpx
#import jwt
from ..models.Notifications import NotificationBase, NotificationCreate, NotificationView, NotificationEvent
from ..db.Notifications_Repository import Notifications_Repository
from ..core import extensions as ext
from datetime import datetime
import uuid
from ..services.Email_Service import EmailService
from logging import getLogger
import ssl
import certifi
from flask import abort

#qué hace el microservicio de verdad
logger = getLogger(__name__)
# FIX SSL 
ssl_context = ssl.create_default_context(cafile=certifi.where())

class Notifications_Service:

    PLAN_RULES = {
        "basico": {"transaction", "login"},
        "estudiante": {"transaction", "login", "scheduled-payment", "fraud-detected"},
        "pro": {
            "transaction",
            "login",
            "scheduled-payment",
            "history-request",
            "fraud-detected",
        },
    }

    ENDPOINTS_HISTORY = {
    "all":      "/v1/transactions/user/{iban}",
    "sent":     "/v1/transactions/user/{iban}/sent",
    "received": "/v1/transactions/user/{iban}/received",
    }

    def __init__(
        self, 
        repository: Notifications_Repository | None = None,
        email_service: EmailService | None = None,
        #users_client: UsersClient | None = None,
        jwt = None
    ):
        self.repo = repository or Notifications_Repository(ext.db)
        self.email_service = email_service or EmailService()
        self.users_client = UsersClient()
        self.jwt = jwt

    def can_send_email(self, plan: str, event_type: str) -> bool:
        return event_type in self.PLAN_RULES.get(plan, set())

    async def handle_event(self, event: NotificationEvent) -> NotificationView:
        """
        Punto único de entrada para eventos desde otros microservicios.
        Construye la notificación, la guarda y envía el email al usuario.
        """
        logger.error(f"EVENT RECIBIDO: {event}")

        metadata = event.metadata or {}
        logger.error(f"despues de metadata")

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
        elif event.type == "transaction":
            amount = metadata.get("amount", "importe desconocido")
            #currency = metadata.get("currency", "EUR")
            recipient = metadata.get("recipient", "destinatario desconocido")
            #timestamp = metadata.get("timestamp", "fecha desconocida")
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

            title = "Pago realizado correctamente"
            message = (
                f"Tu operación se ha completado con éxito.\n\n"
                f"Importe: {amount} \n" #{currency}
                f"Destinatario: {recipient}\n"
                f"Fecha: {timestamp}\n\n"
                f"Puedes consultar el detalle completo desde tu área personal."
            )

        # ----------------------
        # PAGO PROGRAMADO
        # ----------------------
        elif event.type == "scheduled-payment":
            amount = metadata.get("amount")
            date = metadata.get("scheduledDate")
            recipient = metadata.get("recipient")

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
            mode=metadata.get("mode", "all")

            try:
                history_message = await self.send_history_email(
                    user_id=event.userId,
                    mode=metadata.get("mode", "all")
                )

            except PermissionError as e:
                abort(403, description=str(e))

            except ValueError as e:
                abort(400, description=str(e))

            if mode=="sent":
                title = "Tu historial de transferencias enviadas"
            elif mode=="received":
                title = "Tu historial de transferencias recibidas"
            else:
                title = "Tu historial de transferencias completo"

            message = history_message
            skip_generic_email = True
            
        # ======================
        # ANTIFRAUDE
        # ======================
        elif event.type == "fraud-detected":
            reason = metadata.get("reason", "Actividad sospechosa")
            account = metadata.get("account", "Cuenta desconocida")

            title = "Alerta de seguridad: posible fraude detectado"
            message = (
                f"Hemos detectado una actividad sospechosa.\n\n"
                f"Cuenta: {account}\n"
                f"Motivo: {reason}\n\n"
                f"Nuestro equipo está revisando la situación. Te contactaremos si es necesario."
            )

        else:
            raise ValueError(f"Tipo de evento no soportado: {event.type}")


        # Obtener info del usuario
        logger.error("antes de get user")
        user = await self.users_client.get_user_data(self.jwt, event.userId)
        logger.error("después de get user")

        if not isinstance(user, dict):
            logger.warning(f"User data inválido para userId={event.userId}: {user}")
            user = {}
        logger.error(f"USER DATA RAW: {user}")

        #Recogemos el email y el plan del usuario
        email = user.get("email", "nomail@example.com")
        plan = user.get("plan", "pro")

        # Construir la vista de salida
        email_sent = False
        email_reason = None

        #Casuistica para no enviar email genérico al solicitar historial
        skip_generic_email = locals().get("skip_generic_email", False)
        if skip_generic_email:
            email_sent = True
            email_reason = None

        # Enviar email si existe
        elif not self.can_send_email(plan, event.type):
            email_sent = False
            email_reason = (
                f"El plan '{plan}' no permite enviar emails "
                f"para eventos de tipo '{event.type}'"
            )
            logger.info(
                f"Email NO enviado | IBAN={event.userId} | "
                f"plan={plan} | event={event.type} | "
                f"Debido a restricción del plan"
            )
        else:
            if email:
                logger.info(f"Enviando email a {email}")
                await self.email_service.send_notification_email(
                    to_email=email,
                    subject=title,
                    content=message,
                )
                email_sent=True
            else:
                email_sent = False
                email_reason = "El usuario no tiene email registrado"

        # Crear notificación
        notification = NotificationCreate(
            userId=event.userId,
            type=event.type,
            title=title,
            message=message,
            metadata=event.metadata,
            email=email,
            plan=plan,
            email_sent=email_sent,
            email_reason=email_reason
        )

        # Guardar en Mongo
        saved = await self.repo.insert_notification(
            NotificationBase(**notification.model_dump())
        )

        return saved
    
    async def send_history_email(self, user_id: str, mode: str) -> str:
        # 1. Obtener info del usuario
        user = await self.users_client.get_user_data(self.jwt, user_id)

        # from datetime import datetime
        # if not month:
        #     month = datetime.now().strftime("%Y-%m")
        #     logger.error(f"USER DATA en send_history_email: {user} después de asignar month por defecto")

        if not isinstance(user, dict):
            logger.warning(f"User data inválido para userId={user_id}: {user}, se le asignarán datos por defecto")
            user = {}
            #raise ValueError("No se pudo obtener la información del usuario")
            

        email = user.get("email", "nomail@example.com")
        plan = user.get("plan", "pro")
        name = user.get("name", "-")

        # 2. Validar plan
        if plan != "pro":
            logger.info(
                f"Usuario {name} con plan '{plan}' ha intentado solicitar historial"
            )
            raise PermissionError("El plan actual no permite el envío del historial")

        history = await self.fetch_history_from_transactions(
            self.jwt,
            iban=user_id,
            mode=mode
        )

        # 3. Construir email
        message = self.format_history_email_from_service(history, mode)

        # 4. Enviar email
        await self.email_service.send_notification_email(
            to_email=email,
            subject=self.get_subject_by_mode(mode),
            content=message,
        )
        return message
        
    async def fetch_history_from_transactions(self, jwt, iban: str, mode: str):

        path = self.ENDPOINTS_HISTORY.get(mode, self.ENDPOINTS_HISTORY["all"])

        async with httpx.AsyncClient(
            verify=False,
            timeout=5.0
        ) as client:
            headers = {
                 "Authorization": f"{jwt}", # Ya viene con "Bearer ..."
                 "Content-Type": "application/json"
             }
            
            res = await client.get(
                f"http://microservice-transfers:8000{path.format(iban=iban)}",
                headers=headers,
            )
            if res.status_code == 404:
                logger.info(f"No hay movimientos para iban={iban}, mode={mode}")
                return []   # historial vacío válido
            
            res.raise_for_status()
            return res.json()
    
    def format_history_email_from_service(self, history: list[dict], mode: str) -> str:
        if not history:
            return (
                "Has solicitado tu historial de movimientos, "
                "pero no se han encontrado operaciones en el periodo indicado."
            )
        
        intro = {
            "sent": "movimientos enviados",
            "received": "movimientos recibidos",
            "all": "movimientos completo",
        }.get(mode, "movimientos")

        lines = [
            f"Tu historial de {intro}:",
            ""
        ]

        for tx in history:
            # equivalencia:
            raw_date = tx.get("date", "-")
            if raw_date:
                try:
                    date = datetime.fromisoformat(raw_date).strftime("%d/%m/%Y %H:%M")
                except ValueError:
                    date = raw_date  # fallback por si viene algo raro
            else:
                date = "-"
            amount = tx.get("quantity", 0)
            currency = tx.get("currency", "EUR")

            # descripción inteligente
            if mode == "sent":
                model = "enviada"
            elif mode == "received":
                model = "recibida"
            else:
                model = "realizada"
                
            description = f"Transferencia {model} de {tx.get('sender','-')} a {tx.get('receiver','-')}"

            lines.append(
                f"• {date} | {amount} {currency} | {description}"
            )

        lines.append("")
        lines.append(
            "Si no reconoces alguna operación, contacta con tu entidad bancaria."
        )

        return "\n".join(lines)
    
    def get_subject_by_mode(self, mode: str) -> str:
        match mode:
            case "sent":
                return "Historial de transferencias enviadas"
            case "received":
                return "Historial de transferencias recibidas"
            case _:
                return "Historial completo de movimientos"

    def get_mock_history(self, iban: str, month: str) -> dict:
        return {
            "iban": iban,
            "mode": "all",
            "detail": {
                "transactions": [
                    {
                        "date": f"{month}-05T12:30:00.000Z",
                        "amount": 1200,
                        "recipient": "Empresa XYZ",
                    },
                    {
                        "date": f"{month}-12T18:45:00.000Z",
                        "amount": -75.50,  
                        "recipient": "Supermercado ABC",
                    },
                    {
                        "date": f"{month}-20T09:10:00.000Z",
                        "amount": -300,
                        "recipient": "Alquiler vivienda",
                    }
                ]
            }
        }
        
    async def get_all(self) -> list[NotificationView]:
        return await self.repo.get_all_notifications()


    async def update(self, notification_id: str, data: dict):
        return await self.repo.update_notification(notification_id, data)


    async def delete(self, notification_id: str) -> bool:
        return await self.repo.delete_notification(notification_id)
    

class UsersClient:
    async def get_user_data(self, jwt, user_id: str) -> dict | None:
        try:           

            async with httpx.AsyncClient(
                timeout=5.0,
                verify=False
            ) as client:
                
                headers = {
                 "Authorization": f"{jwt}", # Ya viene con "Bearer ..."
                 "Content-Type": "application/json"
             }
                resp = await client.get(
                    f"http://microservice-user-auth:3000/v1/users/{user_id}",
                    headers=headers
                )
                if resp.status_code == 200:
                    return resp.json()

        except Exception as e:
            logger.warning(
                f"No se pudo contactar con user-auth para userId={user_id}: {e}"
            )

        return None
    


    
# MOCK PARA GET EMAIL USER DE USER-AUTH MS
# class UsersClientS:
#     async def get_user_data(self, user_id: str) -> dict:
#         # MOCK para desarrollo / swagger
#         fake_users = {
#             "123": {
#                 "email": "basicuser@example.com",
#                 "subscription": "basico"
#             },
#             "234": {
#                 "email": "studentuser@example.com",
#                 "subscription": "estudiante"
#             },
#             "999": {
#                 "email": "prouser@example.com",
#                 "subscription": "pro"
#             }
#         }

#         return fake_users.get(
#             user_id,
#             {
#                 "email": "default@example.com",
#                 "subscription": "basico"
#             }
#         )

    # def format_history_email(self, metadata: dict) -> str:
    #     transactions = metadata.get("transactions", [])
    #     from_date = metadata.get("from", "—")
    #     to_date = metadata.get("to", "—")
    #     numRecords = len(transactions)

    #     if not transactions:
    #         return (
    #             f"Has solicitado tu historial de movimientos "
    #             f"del {from_date} al {to_date}, pero no se han encontrado operaciones."
    #         )

    #     lines = [
    #         f"Historial de movimientos del {from_date} al {to_date}:",
    #         ""
    #     ]

    #     for tx in transactions:
    #         amount = tx.get("amount", 0)
    #         sign = "+" if amount > 0 else ""
    #         lines.append(
    #             f"• {tx.get('date')} | {sign}{amount} € | {tx.get('description')}"
    #         )

    #     lines.append("")
    #     lines.append("Si no reconoces alguna operación, contacta con tu entidad bancaria.")

    #     return "\n".join(lines)


    



