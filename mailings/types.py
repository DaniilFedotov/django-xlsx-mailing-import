from dataclasses import dataclass
from typing import TypedDict


class MailingRow(TypedDict):
    """Parsed mailing row from spreadsheet."""

    external_id: str
    user_id: str
    email: str
    subject: str
    message: str


@dataclass
class ImportStats:
    """Aggregated counters for one import run."""

    processed: int = 0
    created: int = 0
    skipped: int = 0
    errors: int = 0
