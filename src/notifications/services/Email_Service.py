from httpx import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..core.config import settings
from logging import getLogger
import ssl
import certifi
import os

import urllib.request
from urllib.request import urlopen
import ssl
import json


ssl._create_default_https_context = ssl._create_unverified_context

logger = getLogger(__name__)

# FIX SSL 
#ssl_context = ssl.create_default_context(cafile=certifi.where())
#ssl._create_default_https_context = ssl._create_unverified_context

class EmailService:
    def __init__(self):

        #intenta enviar por SendGrid, si no, se mockea el envío para que igualmente se puedan mostrar los mails en el front
        if settings.SENDGRID_API_KEY == '':
            logger.info("API KEY EN BLANCO")
            self.sg = None 
            self.local_mode = True
        else:
            try:
                # MODO NORMAL - RESPUESTA REAL
                self.sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
                logger.info("Intentando enviar con Sengrid")
                self.local_mode = False
            except:
            # MODO LOCAL - RESPUESTA FAKE
                self.sg = None 
                self.local_mode = True
                logger.info("No se ha conseguido ejecutar SendGridAPIClient, modo LOCAL ACTIVADO")
        
        #self.sg.client._http_client._context = ssl._create_unverified_context()

    async def send_notification_email(self, to_email: str, subject: str, content: str):

        # MODO LOCAL - RESPUESTA FAKE
        if self.local_mode:
            logger.info("LOCAL MODE - email fake OK")
            return {
                "status_code": 202,
                "body": "faketoken",
                "email_sent": True,
                "email": to_email
            }
        else:

            # MODO NORMAL - RESPUESTA REAL
            if not settings.SENDGRID_API_KEY:
                logger.info("SendGrid API key not found - email skipped")
                return  

            try:
                message = Mail(
                    from_email=settings.SENDGRID_FROM_EMAIL,
                    to_emails=to_email,
                    subject=subject,
                    plain_text_content=content
                )

                response = self.sg.send(message)

                logger.info(
                    f"Email enviado a {to_email} con SendGrid| status={response.status_code}"
                )
                logger.debug(response.body)
                logger.debug(response.headers)

                return response
            
            except Exception as e:
                    logger.exception("ERROR sending email with SendGrid")
                    raise