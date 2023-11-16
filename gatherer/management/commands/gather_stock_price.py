from datetime import datetime
from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser

from gatherer.views import get_company_info, gather_stock_price


class Command(BaseCommand):
    """
    Get the stock price
    """
    help = 'Get the stock price'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-s' , '--start' , required=False, type=str, help="Start date")
        parser.add_argument('-e' , '--end' , required=False, type=str, help="End date")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        start_date = options["start"]
        end_date = options["end"]
        if start_date is None or end_date is None:
            start_date = datetime.today()
            end_date = datetime.today()
        else:
            start_date = datetime.strptime(start_date, '%Y%m%d')
            end_date = datetime.strptime(end_date, '%Y%m%d')

        print("======= Start (gather_stock_price) =======")
        gather_stock_price(start_date, end_date)
        print("======= End (gather_stock_price) =======")
