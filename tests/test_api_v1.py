import pytest
import httpx
import logging
from fastapi import APIRouter, HTTPException

BASE_URL = "http://127.0.0.1:8000/v1/notifications/"

# Datos válidos 
valid_notification = {
    "userId": "123",
    "type": "test",
    "title": "Mi título",
    "message": "Hola mundo"
}

@pytest.mark.asyncio
async def test_create_notification_success():
    try:
        async with httpx.AsyncClient() as client:
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

    except Exception as e:
        logging.exception("Failed to create notification")
        raise HTTPException(status_code=500, detail=str(e))
        


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
