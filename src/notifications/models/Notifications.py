from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime

#definición de los datos que entran y salen

# Notificación persistida
class NotificationBase(BaseModel):
    userId: str
    type: Literal["login", "transaction-ok", "transaction-failed"] = Field(..., description="Tipo de notificación")
    title: str | None = None
    message: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)


class NotificationCreate(BaseModel):
    userId: str
    type: Literal["login", "transaction-ok", "transaction-failed"]
    title: str | None = None
    message: str

class NotificationView(BaseModel):
    model_config = {"populate_by_name": True}

    id: str = Field(alias="_id")
    userId: str
    type: str
    title: str | None
    message: str
    createdAt: datetime

# Evento entrante (desde otros MS)
class NotificationEvent(BaseModel):
    userId: str
    type: Literal["login", "transaction-ok", "transaction-failed"]
    success: bool | None = None
    email: str | None




