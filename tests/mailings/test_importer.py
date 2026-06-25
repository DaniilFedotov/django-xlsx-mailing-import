from unittest.mock import patch

import pytest
from django.core.management import call_command
from openpyxl import Workbook

from mailings.exceptions import MissingColumnsError
from mailings.importer import import_mailings_from_xlsx
from mailings.models import MailingRecord
from mailings.types import ImportStats


def _write_xlsx(path, rows: list[list[object]]) -> None:
    workbook = Workbook()
    worksheet = workbook.active
    for row in rows:
        worksheet.append(row)
    workbook.save(path)


@pytest.mark.django_db
@patch("mailings.importer.send_email")
def test_import_creates_records(mock_send_email, tmp_path):
    file_path = tmp_path / "mailings.xlsx"
    _write_xlsx(
        file_path,
        [
            ["external_id", "user_id", "email", "subject", "message"],
            ["ext-1", 1, "user1@example.com", "Hello", "Message 1"],
            ["ext-2", 2, "user2@example.com", "Hi", "Message 2"],
        ],
    )

    stats = import_mailings_from_xlsx(str(file_path))

    assert stats.processed == 2
    assert stats.created == 2
    assert stats.skipped == 0
    assert stats.errors == 0
    assert MailingRecord.objects.count() == 2
    assert mock_send_email.call_count == 2


@pytest.mark.django_db
@patch("mailings.importer.send_email")
def test_import_skips_duplicate_external_id(mock_send_email, tmp_path):
    file_path = tmp_path / "mailings.xlsx"
    rows = [
        ["external_id", "user_id", "email", "subject", "message"],
        ["ext-1", 1, "user1@example.com", "Hello", "Message 1"],
    ]
    _write_xlsx(file_path, rows)

    first_stats = import_mailings_from_xlsx(str(file_path))
    second_stats = import_mailings_from_xlsx(str(file_path))

    assert first_stats.created == 1
    assert second_stats.skipped == 1
    assert second_stats.created == 0
    assert mock_send_email.call_count == 1


@pytest.mark.django_db
@patch("mailings.importer.send_email")
def test_import_counts_invalid_rows(mock_send_email, tmp_path):
    file_path = tmp_path / "mailings.xlsx"
    _write_xlsx(
        file_path,
        [
            ["external_id", "user_id", "email", "subject", "message"],
            ["ext-bad", 1, "not-an-email", "Hello", "Message"],
            ["ext-ok", 2, "ok@example.com", "Hi", "Valid"],
        ],
    )

    stats = import_mailings_from_xlsx(str(file_path))

    assert stats.processed == 2
    assert stats.created == 1
    assert stats.errors == 1
    assert mock_send_email.call_count == 1


@pytest.mark.django_db
@patch("mailings.importer.send_email")
def test_import_command_prints_stats(mock_send_email, tmp_path):
    file_path = tmp_path / "mailings.xlsx"
    _write_xlsx(
        file_path,
        [
            ["external_id", "user_id", "email", "subject", "message"],
            ["ext-1", 1, "user1@example.com", "Hello", "Message"],
        ],
    )

    call_command("import_mailings", str(file_path))

    assert MailingRecord.objects.count() == 1
    assert mock_send_email.call_count == 1


@pytest.mark.django_db
@patch("mailings.importer.send_email")
def test_reimport_skips_all_existing_rows(mock_send_email, tmp_path):
    file_path = tmp_path / "mailings.xlsx"
    _write_xlsx(
        file_path,
        [
            ["external_id", "user_id", "email", "subject", "message"],
            ["ext-1", 1, "a@example.com", "S1", "M1"],
            ["ext-2", 2, "b@example.com", "S2", "M2"],
            ["ext-3", 3, "c@example.com", "S3", "M3"],
        ],
    )

    first_stats = import_mailings_from_xlsx(str(file_path))
    second_stats = import_mailings_from_xlsx(str(file_path))

    assert first_stats == ImportStats(processed=3, created=3, skipped=0, errors=0)
    assert second_stats == ImportStats(processed=3, created=0, skipped=3, errors=0)
    assert mock_send_email.call_count == 3


@pytest.mark.django_db
@patch("mailings.importer.send_email")
def test_duplicate_external_id_within_same_file_is_skipped(mock_send_email, tmp_path):
    file_path = tmp_path / "mailings.xlsx"
    _write_xlsx(
        file_path,
        [
            ["external_id", "user_id", "email", "subject", "message"],
            ["ext-dup", 1, "first@example.com", "First", "First row"],
            ["ext-dup", 2, "second@example.com", "Second", "Duplicate in file"],
        ],
    )

    stats = import_mailings_from_xlsx(str(file_path))

    assert stats.processed == 2
    assert stats.created == 1
    assert stats.skipped == 1
    assert stats.errors == 0
    assert mock_send_email.call_count == 1


@pytest.mark.django_db
def test_empty_workbook_returns_zero_stats(tmp_path):
    file_path = tmp_path / "empty.xlsx"
    _write_xlsx(file_path, [])

    stats = import_mailings_from_xlsx(str(file_path))

    assert stats == ImportStats()


@pytest.mark.django_db
def test_missing_required_columns_raises(tmp_path):
    file_path = tmp_path / "bad_header.xlsx"
    _write_xlsx(
        file_path,
        [
            ["external_id", "email"],
            ["ext-1", "user@example.com"],
        ],
    )

    with pytest.raises(MissingColumnsError):
        import_mailings_from_xlsx(str(file_path))
