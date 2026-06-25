from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import Workbook

from mailings.management.demo_data import SAMPLE_FILES


class Command(BaseCommand):
    """Generate sample XLSX files for manual import testing."""

    help = "Generate sample XLSX files for manual import testing."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "variant",
            nargs="?",
            choices=["valid", "invalid", "all"],
            default="all",
            help="Which sample file(s) to generate (default: all).",
        )
        parser.add_argument(
            "--output-dir",
            default=str(settings.BASE_DIR),
            help="Directory for output files (default: project root).",
        )

    def handle(self, *args, **options) -> None:
        output_dir = Path(options["output_dir"])
        variant = options["variant"]

        variants = list(SAMPLE_FILES.keys()) if variant == "all" else [variant]
        for sample_variant in variants:
            filename, rows = SAMPLE_FILES[sample_variant]
            output_path = output_dir / filename
            self._write_xlsx(output_path, rows)
            self.stdout.write(f"Created: {output_path}")

    @staticmethod
    def _write_xlsx(output_path: Path, rows: list[list[object]]) -> None:
        workbook = Workbook()
        worksheet = workbook.active
        for row in rows:
            worksheet.append(row)
        workbook.save(output_path)
