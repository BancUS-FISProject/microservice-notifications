from quart import Blueprint, request
from quart_schema import validate_request, validate_response, tag

from ...services.Email_Service import EmailService
from ...models.Notifications import NotificationCreate, NotificationView, NotificationEvent
from ...services.Notifications_Service import Notifications_Service
from ...db.Notifications_Repository import Notifications_Repository
from ...core import extensions as ext
from logging import getLogger
from ...core.config import settings

logger = getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

bp = Blueprint("notifications_bp_v1", __name__, url_prefix="/v1/notifications")

# ------------------------
# POST: crear notificación
# ------------------------
@bp.post("/")
@tag(["Notifications - Crear"])
@validate_request(NotificationCreate)
#@validate_response(NotificationView, 201)
async def create_notification(data: NotificationCreate):
    try:
        repo = Notifications_Repository(ext.db)
        service = Notifications_Service(repo)
        
        logger.info("Received new notification")
        result = await service.register_event(data)
        #return result, 201
        return result.model_dump(by_alias=False), 201

    except Exception as e:
        import traceback
        print("ERROR EN /v1/notifications")
        print(traceback.format_exc())
        raise


# ------------------------
# GET: obtener todas
# ------------------------
#@bp.get("/all")
#@tag(["Notifications - Listar todas"])
#@validate_response(list[NotificationView], 200)
#async def list_notifications():
 #   repo = Notifications_Repository(ext.db)
 #   service = Notifications_Service(repo)
 #   logger.info("Fetching all notifications")
 #   result = await service.get_all()
 #   return result


# ------------------------
# GET por usuario
# ------------------------
#@bp.get("/user/<userId>")
#@tag(["Notifications - Por usuario"])
#async def get_notifications(userId: str):
#    repo = Notifications_Repository(ext.db)
#    notifications = await repo.get_notifications_by_user(userId)
#    return notifications


# ------------------------
# POST login event
# ------------------------
@bp.post("/login")
@validate_request(NotificationCreate)
@validate_response(NotificationView, 201)
@tag(["Eventos - Login"])
async def notification_login(data: NotificationCreate):
    body = await request.get_json()

    data = NotificationCreate(
        userId=body["userId"],
        message=body.get("message", "Inicio de sesión"),
        type="login"
    )

    service = Notifications_Service()
    result = await service.register_event(data)
    return result


# ------------------------
# POST transaction event
# ------------------------
@bp.post("/transaction")
@validate_request(NotificationCreate)
@validate_response(NotificationView, 201)
@tag(["Eventos - Transacciones"])
async def notification_transaction():
    body = await request.get_json()
    success = body.get("success", True)
    notif_type = "transaction-ok" if success else "transaction-failed"

    data = NotificationCreate(
        userId=body["userId"],
        message=body.get("message", "Movimiento en tu cuenta"),
        type=notif_type
    )

    service = Notifications_Service()
    result = await service.register_event(data)
    return result


# ======================================================
# EVENTOS DESDE OTROS MICROSERVICIOS
# ======================================================
@bp.post("/events")
@tag(["Eventos"])
@validate_request(NotificationEvent)
@validate_response(NotificationView, 201)
async def receive_event(data: NotificationEvent):

    if data.type == "login":
        title = "Nuevo inicio de sesión"
        message = "Se ha detectado un inicio de sesión en tu cuenta"

    elif data.type == "transaction-ok":
        if data.success:
            title = "Pago realizado"
            message = "Tu pago se ha completado correctamente"
        elif data.type == "transaction-failed":
            title = "Pago rechazado"
            message = "No se ha podido completar tu pago"

    notification = NotificationCreate(
        userId=data.userId,
        type=data.type,
        title=title,
        message=message
    )
    service = Notifications_Service()
    #return await service.register_event(notification)
    return await service.register_event(
        notification,
        user_email=data.email
    )

# ======================================================
# CONSULTA DE NOTIFICACIONES (FRONTEND)
# ======================================================
@bp.get("/user/<userId>")
@tag(["Consulta - Usuario"])
@validate_response(list[NotificationView], 200)
async def get_notifications_by_user(userId: str):
    """
    Devuelve todas las notificaciones de un usuario,
    ordenadas por fecha.
    """
    repo = Notifications_Repository(ext.db)
    notifications = await repo.get_notifications_by_user(userId)
    return notifications


# ======================================================
# CONSULTA GLOBAL (ADMIN / DEBUG)
# ======================================================
@bp.get("/")
@tag(["Consulta - Admin"])
@validate_response(list[NotificationView], 200)
async def get_all_notifications():
    """
    Devuelve todas las notificaciones del sistema.
    Endpoint pensado para administración o debugging.
    """
    service = Notifications_Service(
        Notifications_Repository(ext.db)
    )
    return await service.get_all()


# ------------------------
# PUT: actualizar notificación
# ------------------------
#@bp.put("/<notification_id>")
#@tag(["Notifications - Update"])
#@validate_request(NotificationUpdate)
#async def update_notification(notification_id: str, data: NotificationUpdate):
 #   service = Notifications_Service()
 #   updated = await service.update(
 #       notification_id,
 #       data.model_dump(exclude_none=True)
 #   )

 #   if not updated:
 #       return {"error": "Notification not found"}, 404

 #   return updated, 200


# ------------------------
# DELETE: eliminar notificación
# ------------------------
@bp.delete("/<notification_id>")
@tag(["Notifications - Delete"])
async def delete_notification(notification_id: str):
    service = Notifications_Service()
    deleted = await service.delete(notification_id)

    if not deleted:
        return {"error": "Notification not found"}, 404

    return {"status": "deleted"}, 200


# ------------------------
# POST: test email
# ------------------------
@bp.post("/test-email")
async def test_email():
    try:
        email_service = EmailService()

        await email_service.send_notification_email(
            to_email="elenaberdu@gmail.com",
            subject="Test Notifications Service",
            content="Este es un email de prueba desde Notifications MS"
        )

        return {"status": "email sent"}

    except Exception as e:
        import traceback
        print("ERROR EN TEST EMAIL")
        print(traceback.format_exc())
        return {"error": str(e)}, 500