from quart import Blueprint, abort, jsonify, request
from quart_schema import validate_request, validate_response, tag

from ...services.Email_Service import EmailService
from ...models.Notifications import NotificationCreate, NotificationView, NotificationEvent, NotificationUpdate
from ...services.Notifications_Service import Notifications_Service
from ...db.Notifications_Repository import Notifications_Repository
from ...core import extensions as ext
from logging import getLogger
from ...core.config import settings
import jwt

logger = getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

bp = Blueprint("notifications_bp_v1", __name__, url_prefix="/v1/notifications")
DEFAULT_JWT = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"

# ======================================================
# EVENTOS DESDE OTROS MICROSERVICIOS (CORE)
# ======================================================
@bp.post("/events")
@tag(["Eventos"])
@validate_request(NotificationEvent)
@validate_response(NotificationView, 201)
async def receive_event(data: NotificationEvent):
    """
    Endpoint principal del microservicio.
    Recibe eventos desde otros MS (login, pagos, etc).
    """
    
    # 1. Obtener el header Authorization
    auth_header = request.headers.get('Authorization') or DEFAULT_JWT
    logger.debug(f"TOKEN RAW RECIBIDO events: {auth_header}")
    logger.debug(f"HEADERS ENTRANTES event: {dict(request.headers)}")
    if not auth_header:
        return jsonify({"error": "Falta el header Authorization"}), 401
    
    # 5. Continuamos con la lógica del endpoint
    service = Notifications_Service(jwt=auth_header)  # jwt=auth_header)
    result = await service.handle_event(data)
    return result, 201


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

    # 1. Obtener el header Authorization
    auth_header = request.headers.get('Authorization') or DEFAULT_JWT
    logger.debug(f"TOKEN RAW RECIBIDO list: {auth_header}")
    logger.debug(f"HEADERS ENTRANTES list: {dict(request.headers)}")
    if not auth_header:
        return jsonify({"error": "Falta el header Authorization"}), 401
    
    # 5. Continuamos con la lógica del endpoint
    repo = Notifications_Repository(ext.db)  # jwt=auth_header)
    return await repo.get_notifications_by_user(userId)

# ======================================================
# CONSULTA GLOBAL (ADMIN)
# ======================================================
@bp.get("/")
@tag(["Consulta - Admin"])
@validate_response(list[NotificationView], 200)
async def get_all_notifications():
    """
    Devuelve todas las notificaciones del sistema.
    Endpoint de administración o debugging.
    """
    service = Notifications_Service(
        Notifications_Repository(ext.db)
    )
    return await service.get_all()


# ======================================================
# DELETE NOTIFICATION (ADMIN)
# ======================================================
@bp.delete("/<notification_id>")
@tag(["Admin - Delete"])
async def delete_notification(notification_id: str):
    service = Notifications_Service()
    deleted = await service.delete(notification_id)

    if not deleted:
        return {"error": "Notification not found"}, 404

    return {"status": "deleted"}, 200


# ------------------------
# PUT: actualizar notificación
# ------------------------
@bp.put("/<notification_id>")
@tag(["Notifications - Update"])
@validate_request(NotificationUpdate)
async def update_notification(notification_id: str, data: NotificationUpdate):
   service = Notifications_Service()
   updated = await service.update(
       notification_id,
       data.model_dump(exclude_none=True)
   )

   if not updated:
       return {"error": "Notification not found"}, 404

   return updated, 200



# ======================================================
# TEST EMAIL (DEBUG)
# ======================================================
@bp.post("/test-email")
@tag(["Debug"])
async def test_email():
    """
    Endpoint de prueba para verificar SendGrid.
    """
    email_service = EmailService()

    await email_service.send_notification_email(
        to_email="elenaberdu@gmail.com",
        subject="Test Notifications Service",
        content="Este es un email de prueba desde Notifications MS"
    )

    return {"status": "email sent"}

# ======================================================
# HEALTH
# ======================================================
@bp.get("/health")
@tag(["Health"])
async def health_check():
 
    return {"status": "ok", "service": "notifications"}, 200



def decode_jwt(token):
    return jwt.decode(token, options={"verify_signature": False})

# ------------------------
# POST: crear notificación
# ------------------------
#@bp.post("/")
#@tag(["Notifications - Crear"])
#@validate_request(NotificationCreate)
#async def create_notification(data: NotificationCreate):
#    try:
#        repo = Notifications_Repository(ext.db)
#        service = Notifications_Service(repo)
#
#        logger.info("Received new notification")
#        result = await service.register_event(data)
#        #return result, 201
#        return result.model_dump(by_alias=False), 201

#    except Exception as e:
#        import traceback
#        print("ERROR EN /v1/notifications")
#        print(traceback.format_exc())
#        raise


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
#@bp.post("/login")
#@validate_request(NotificationCreate)
#@validate_response(NotificationView, 201)
#@tag(["Eventos - Login"])
#async def notification_login(data: NotificationCreate):
#    body = await request.get_json()

#    data = NotificationCreate(
#        userId=body["userId"],
#        message=body.get("message", "Inicio de sesión"),
#        type="login"
#    )

#    service = Notifications_Service()
#    result = await service.register_event(data)
#    return result


# ------------------------
# POST transaction event
# ------------------------
#@bp.post("/transaction")
#@validate_request(NotificationCreate)
#@validate_response(NotificationView, 201)
#@tag(["Eventos - Transacciones"])
#async def notification_transaction():
#    body = await request.get_json()
#    success = body.get("success", True)
#    notif_type = "transaction-ok" if success else "transaction-failed"

#    data = NotificationCreate(
#        userId=body["userId"],
#        message=body.get("message", "Movimiento en tu cuenta"),
#        type=notif_type
#    )
#    service = Notifications_Service()
#    result = await service.register_event(data)
#    return result