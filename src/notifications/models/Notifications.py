from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# =====================================================
# MODELO BASE DE NOTIFICACIÓN
# =====================================================
class NotificationBase(BaseModel):
    """
    Modelo base que representa una notificación persistida
    en el sistema de almacenamiento.
    """

    userId: str = Field(
        ...,
        description="IBAN identificador del usuario al que pertenece la notificación."
    )

    email: Optional[EmailStr] | None = Field(
        None,
        description="Dirección de correo electrónico del usuario. Puede ser nula si no está disponible."
    )

    type: Literal[
        "login",
        "transaction",
        "scheduled-payment",
        "history-request",
        "fraud-detected"
    ] = Field(
        ...,
        description="Tipo de evento que origina la notificación."
    )

    plan: Optional[Literal["basico", "premium", "pro"]] = Field(
        None,
        description="Plan de suscripción del usuario en el momento del evento."
    )

    title: Optional[str] = Field(
        None,
        description="Título breve de la notificación."
    )

    message: str = Field(
        ...,
        description="Mensaje principal que se mostrará al usuario."
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description=(
            "Información adicional asociada al evento. "
            "Su estructura es flexible y depende del microservicio emisor."
        )
    )

    email_sent: Optional[bool] = Field(
        None,
        description="Indica si se ha enviado un correo electrónico asociado a la notificación."
    )

    email_reason: Optional[str] = Field(
        None,
        description="Motivo por el cual se ha enviado (o no) el correo electrónico."
    )

    createdAt: datetime = Field(
        default_factory=datetime.utcnow,
        description="Marca temporal de creación de la notificación."
    )


# =====================================================
# ENTRADA AL SERVICIO (ANTES DE PERSISTIR)
# =====================================================
class NotificationCreate(BaseModel):
    """
    Payload utilizado para crear una notificación antes de
    ser almacenada en base de datos.
    """

    userId: str = Field(
        ...,
        description="IBAN identificador del usuario destinatario de la notificación."
    )

    email: Optional[EmailStr] | None = Field(
        None,
        description="Correo electrónico del usuario. Se utiliza para el envío de emails si aplica."
    )

    type: Literal[
        "login",
        "transaction",
        "scheduled-payment",
        "history-request",
        "fraud-detected"
    ] = Field(
        ...,
        description="Tipo de evento que genera la notificación."
    )

    plan: Optional[Literal["basico", "premium", "pro"]] = Field(
        None,
        description="Plan de suscripción del usuario."
    )

    title: Optional[str] = Field(
        None,
        description="Título corto que resume la notificación."
    )

    message: str = Field(
        ...,
        description="Contenido principal de la notificación."
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Datos contextuales adicionales del evento."
    )

    email_sent: Optional[bool] = Field(
        None,
        description="Indica si se ha enviado un correo electrónico asociado."
    )

    email_reason: Optional[str] = Field(
        None,
        description="Razón por la que se envía (o no) el correo electrónico."
    )


# =====================================================
# RESPUESTA DE LA API
# =====================================================
class NotificationView(BaseModel):
    """
    Vista de lectura de una notificación devuelta por la API.
    """

    model_config = {"populate_by_name": True}

    id: str = Field(
        alias="_id",
        description="Identificador único de la notificación."
    )

    userId: str = Field(
        ...,
        description="IBAN identificador del usuario propietario de la notificación."
    )

    email: Optional[EmailStr] | None = Field(
        None,
        description="Correo electrónico asociado al usuario."
    )

    plan: Optional[str] = Field(
        None,
        description="Plan de suscripción del usuario."
    )

    type: Optional[str] = Field(
        None,
        description="Tipo de evento que originó la notificación."
    )

    title: Optional[str] = Field(
        None,
        description="Título de la notificación."
    )

    message: str = Field(
        ...,
        description="Contenido principal de la notificación."
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Información adicional asociada a la notificación."
    )

    email_sent: Optional[bool] = Field(
        None,
        description="Indica si se ha enviado un correo electrónico al usuario."
    )

    email_reason: Optional[str] = Field(
        None,
        description="Motivo del envío o no del correo electrónico."
    )

    createdAt: datetime = Field(
        ...,
        description="Fecha y hora de creación de la notificación."
    )


# =====================================================
# EVENTO ENTRANTE DESDE OTROS MICROSERVICIOS
# =====================================================
class NotificationEvent(BaseModel):
    """
    Test evento recibido desde otros microservicios del sistema.
    """

    userId: str = Field(
        ...,
        description="IBAN identificador del usuario que ha generado el evento."
    )

    type: Literal[
        "login",
        "transaction",
        "scheduled-payment",
        "history-request",
        "fraud-detected"
    ] = Field(
        ...,
        description="Tipo de evento que debe ser procesado por el servicio de notificaciones."
    )

    plan: Optional[Literal["basico", "premium", "pro"]] = Field(
        None,
        description="Plan de suscripción del usuario en el momento del evento."
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Información contextual adicional enviada por el microservicio emisor."
    )


# =====================================================
# UPDATE DE NOTIFICACIÓN
# =====================================================
class NotificationUpdate(BaseModel):
    """
    Payload utilizado para actualizar parcialmente una notificación existente.
    """

    title: Optional[str] = Field(
        None,
        description="Nuevo título de la notificación."
    )

    message: Optional[str] = Field(
        None,
        description="Nuevo contenido del mensaje."
    )

    type: Optional[Literal[
        "login",
        "transaction",
        "scheduled-payment",
        "history-request",
        "fraud-detected"
    ]] = Field(
        None,
        description="Nuevo tipo de evento asociado a la notificación."
    )

    plan: Optional[Literal["basico", "premium", "pro"]] = Field(
        None,
        description="Nuevo plan de suscripción del usuario."
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Información contextual adicional actualizada."
    )

    email_sent: Optional[bool] = Field(
        None,
        description="Indica si el correo electrónico ha sido enviado."
    )

    email_reason: Optional[str] = Field(
        None,
        description="Motivo actualizado del envío o no del correo electrónico."
    )
