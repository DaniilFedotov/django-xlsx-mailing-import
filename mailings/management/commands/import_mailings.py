from django.core.management.base import BaseCommand, CommandError

from mailings.exceptions import MissingColumnsError
from mailings.importer import import_mailings_from_xlsx


class Command(BaseCommand):
    """Import mailing rows from an XLSX file and send emails."""

    help = "Import mailings from XLSX file and send emails for new records."

    def add_arguments(self, parser) -> None:
        parser.add_argument("file_path", type=str, help="Path to the XLSX file.")

    def handle(self, *args, **options) -> None:
        file_path = options["file_path"]

        try:
            stats = import_mailings_from_xlsx(file_path)
        except FileNotFoundError as exc:
            raise CommandError(f"File not found: {file_path}") from exc
        except MissingColumnsError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(f"Processed rows: {stats.processed}")
        self.stdout.write(f"Created records: {stats.created}")
        self.stdout.write(f"Skipped records: {stats.skipped}")
        self.stdout.write(f"Error rows: {stats.errors}")
