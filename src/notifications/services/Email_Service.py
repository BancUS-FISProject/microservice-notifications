from httpx import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..core.config import settings
from logging import getLogger
import ssl
import certifi
import os


logger = getLogger(__name__)
# FIX SSL 
ssl_context = ssl.create_default_context(cafile=certifi.where())
#ssl._create_default_https_context = ssl._create_unverified_context

class EmailService:
    def __init__(self):
        self.enabled = os.getenv("EMAIL_ENABLED", "true").lower() == "true"
        if not self.enabled:
            return
        self.sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    async def send_notification_email(self, to_email: str, subject: str, content: str):
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