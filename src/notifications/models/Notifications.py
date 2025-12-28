from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# =====================================================
# MODELO PERSISTIDO (BASE DE DATOS)
# =====================================================
class NotificationBase(BaseModel):
    userId: str
    email: EmailStr

    type: Literal[
        "login",
        "transaction-ok",
        "transaction-failed",
        "scheduled-payment"
    ]

    title: Optional[str] = None
    message: str

    # Datos específicos del evento (flexible)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    createdAt: datetime = Field(default_factory=datetime.utcnow)


# =====================================================
# ENTRADA AL SERVICIO (ANTES DE PERSISTIR)
# =====================================================
class NotificationCreate(BaseModel):
    userId: str
    email: EmailStr

    type: Literal[
        "login",
        "transaction-ok",
        "transaction-failed",
        "scheduled-payment"
    ]

    title: Optional[str] = None
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


# =====================================================
# RESPUESTA DE LA API
# =====================================================
class NotificationView(BaseModel):
    model_config = {"populate_by_name": True}

    id: str = Field(alias="_id")

    userId: str
    email: EmailStr

    type: str
    title: Optional[str]
    message: str
    metadata: Dict[str, Any]

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
        "scheduled-payment"
    ]

    # Información contextual del evento
    metadata: Dict[str, Any] = Field(default_factory=dict)
