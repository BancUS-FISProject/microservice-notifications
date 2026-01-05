from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# =====================================================
# MODELO PERSISTIDO (BASE DE DATOS)
# =====================================================
class NotificationBase(BaseModel):
    userId: str
    email: Optional[EmailStr] | None

    type: Literal[
        "login",
        "transaction-ok",
        "transaction-failed",
        "scheduled-payment",
        "history-request",
        "fraud-detected"
    ]
    plan: Optional[Literal["basic", "premium", "business"]] = None
    title: Optional[str] = None
    message: str
    # Datos específicos del evento (flexible)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    email_sent: Optional[bool] = None
    email_reason: Optional[str] = None

    createdAt: datetime = Field(default_factory=datetime.utcnow)


# =====================================================
# ENTRADA AL SERVICIO (ANTES DE PERSISTIR)
# =====================================================
class NotificationCreate(BaseModel):
    userId: str
    email: Optional[EmailStr] | None

    type: Literal[
        "login",
        "transaction-ok",
        "transaction-failed",
        "scheduled-payment",
        "history-request",
        "fraud-detected"
    ]
    plan: Optional[Literal["basic", "premium", "business"]] = None
    title: Optional[str] = None
    message: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    email_sent: Optional[bool] = None
    email_reason: Optional[str] = None


# =====================================================
# RESPUESTA DE LA API
# =====================================================
class NotificationView(BaseModel):
    model_config = {"populate_by_name": True}

    id: str = Field(alias="_id")

    userId: str
    email: Optional[EmailStr] | None
    plan: Optional[str] = None
    type: str
    title: Optional[str]
    message: str
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    email_sent: Optional[bool] = None
    email_reason: Optional[str] = None

    createdAt: datetime


# =====================================================
# EVENTO ENTRANTE DESDE OTROS MICROSERVICIOS
# =====================================================
class NotificationEvent(BaseModel):
    userId: str

    type: Literal[
        "login",
        "transaction-ok",
        "transaction-failed",
        "scheduled-payment",
        "history-request",
        "fraud-detected"
    ]
    plan: Optional[Literal["basic", "premium", "business"]] = None

    # Información contextual del evento
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

# =====================================================
# UPDATE DE NOTIFICACIÓN
# =====================================================
class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[Literal[
        "login",
        "transaction-ok",
        "transaction-failed",
        "scheduled-payment",
        "history-request",
        "fraud-detected"
    ]] = None
    plan: Literal["basic", "premium", "business"] | None = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    email_sent: Optional[bool] = None
    email_reason: Optional[str] = None