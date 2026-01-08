import pytest
import httpx
from src.notifications.core import extensions as ext


BASE_URL = "http://127.0.0.1:8000/v1/notifications/"

# Datos válidos 
valid_notification = {
    "userId": "123",
    "type": "login",
    "title": "Mi título",
    "message": "Hola mundo"
}

@pytest.mark.asyncio
async def test_create_notification_success():

    #await ext.init_db_client() 

    async with httpx.AsyncClient(timeout=10.0) as client:

        response = await client.post(BASE_URL, json=valid_notification)

        #assert response.status_code == 201, "Create notif fail"
        assert response.status_code == 201, response.text

        data = response.json()
        # Comprobamos que los datos devueltos coincidan
        assert data["userId"] == valid_notification["userId"]
        assert data["type"] == valid_notification["type"]
        assert data["title"] == valid_notification["title"]
        assert data["message"] == valid_notification["message"]
        assert "id" in data  # Mongo devuelve el id como string

    #await ext.close_db_client()
    


@pytest.mark.asyncio
async def test_create_notification_missing_field():
    async with httpx.AsyncClient() as client:
        # Enviamos un JSON incompleto para que falle
        response = await client.post(
            BASE_URL,
            json={"userId": "123"}  
        )
        # Debe dar 400 porque Pydantic valida los campos obligatorios
        assert response.status_code == 400
