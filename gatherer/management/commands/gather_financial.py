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
        parser.add_argument('-s' , '--start' , required=False, type=str, help="Start year")
        parser.add_argument('-e' , '--end' , required=False, type=str, help="End year")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        start_date = options["start"]
        end_date = options["end"]
        if start_date is None or end_date is None:
            start_date = datetime.today()
            end_date = datetime.today()
        else:
            start_date = datetime.strptime(start_date, '%Y%m%d')
            end_date = datetime.strptime(end_date, '%Y%m%d')

        print("======= Start (gather_financial_data) =======")
        gather_financial_data(start_date, end_date)
        print("======= End (gather_financial_data) =======")
