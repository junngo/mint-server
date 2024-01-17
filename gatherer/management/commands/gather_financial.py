from datetime import datetime
from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser

from gatherer.views import gather_financial_data


class Command(BaseCommand):
    """
    Gather the financial_data
    """
    help = "Gather the financial data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-y', '--year', required=False, type=str, help="Search year")
        parser.add_argument('-c', '--company', required=False, type=str, help="Company Code")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        year = options["year"]
        company_code = options["company"]
        if year is None:
            year = datetime.now().strftime("%Y")

        print("======= Start (gather_financial_data) =======")
        gather_financial_data(year, company_code)
        print("======= End (gather_financial_data) =======")
