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
        self.enabled = os.getenv("EMAIL_ENABLED", "true").lower() == "true"
        if not self.enabled:
            return
        # MODO LOCAL
        self.local_mode = True #os.getenv("SENDGRID_LOCAL_MODE")

        if not self.enabled:
            return

        if self.local_mode:
            self.sg = None   # no se crea cliente real
        else:
            #antes, solo esto: 
            self.sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        #self.sg.client._http_client._context = ssl._create_unverified_context()

    async def send_notification_email(self, to_email: str, subject: str, content: str):

        # MODO LOCAL → RESPUESTA FAKE
        if self.local_mode:
            logger.info("LOCAL MODE - email fake OK")
            return {
                "status_code": 202,
                "body": "faketoken",
                "email_sent": True,
                "email": to_email
            }
        else:

            #normal sendgrid email sending
            if not settings.SENDGRID_API_KEY:
                logger.info("SendGrid API key not found - email skipped")
                return  
            if not self.enabled:
                return {"status": "email disabled"}
            try:
                message = Mail(
                    from_email=settings.SENDGRID_FROM_EMAIL,
                    to_emails=to_email,
                    subject=subject,
                    plain_text_content=content
                )

                response = self.sg.send(message)

                logger.info(
                    f"Email enviado a {to_email} | status={response.status_code}"
                )
                logger.debug(response.body)
                logger.debug(response.headers)

                return response
            
            except Exception as e:
                    logger.exception("ERROR sending email with SendGrid")
                    raise