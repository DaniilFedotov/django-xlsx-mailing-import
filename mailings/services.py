import logging
import random
from time import sleep

from django.conf import settings

logger = logging.getLogger(__name__)


def send_email(email: str, subject: str, message: str) -> None:
    """Simulate email delivery by waiting and writing the message to the log."""
    delay = random.randint(
        settings.MAILING_SEND_DELAY_MIN,
        settings.MAILING_SEND_DELAY_MAX,
    )
    sleep(delay)
    logger.info("Send EMAIL to %s | subject=%s | message=%s", email, subject, message)
