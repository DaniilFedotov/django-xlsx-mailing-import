from unittest.mock import patch

import pytest
from django.test import override_settings

from mailings.services import send_email


@override_settings(MAILING_SEND_DELAY_MIN=5, MAILING_SEND_DELAY_MAX=20)
@patch("mailings.services.logger")
@patch("mailings.services.sleep")
@patch("mailings.services.random.randint", return_value=7)
def test_send_email_logs_message(mock_randint, mock_sleep, mock_logger):
    send_email("user@example.com", "Subject", "Body")

    mock_randint.assert_called_once_with(5, 20)
    mock_sleep.assert_called_once_with(7)
    mock_logger.info.assert_called_once()
