from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..core.config import settings
from logging import getLogger

logger = getLogger(__name__)

class EmailService:
    def __init__(self):
        self.sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

    async def send_notification_email(
        self,
        to_email: str,
        subject: str,
        content: str
    ):
        message = Mail(
            from_email=settings.SENDGRID_FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )

        try:
            response = self.sg.send(message)
            logger.info(f"Email sent to {to_email}")
            return response.status_code
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return None
