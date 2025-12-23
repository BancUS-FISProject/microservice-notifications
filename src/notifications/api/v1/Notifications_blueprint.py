from quart import Blueprint, request
from quart_schema import validate_request, validate_response, tag
from ...models.Notifications import NotificationCreate, NotificationView
from ...services.Notifications_Service import Notifications_Service
from ...db.Notifications_Repository import Notifications_Repository
from ...core import extensions as ext
from logging import getLogger
#from ...core.config import settings

logger = getLogger(__name__)
#logger.setLevel(settings.LOG_LEVEL)

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
        return result

    except Exception as e:
        import traceback
        print("ERROR EN /v1/notifications")
        print(traceback.format_exc())
        raise


# ------------------------
# GET: obtener todas
# ------------------------
@bp.get("/all")
@tag(["Notifications - Listar todas"])
@validate_response(list[NotificationView], 200)
async def list_notifications():
    repo = Notifications_Repository(ext.db)
    service = Notifications_Service(repo)
    logger.info("Fetching all notifications")
    result = await service.get_all()
    return result


# ------------------------
# GET por usuario
# ------------------------
@bp.get("/user/<userId>")
@tag(["Notifications - Por usuario"])
async def get_notifications(userId: str):
    repo = Notifications_Repository(ext.db)
    notifications = await repo.get_notifications_by_user(userId)
    return notifications


# ------------------------
# POST login event
# ------------------------
@bp.post("/login")
@validate_request(NotificationCreate)
@validate_response(NotificationView, 201)
@tag(["Eventos - Login"])
async def notification_login():
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
