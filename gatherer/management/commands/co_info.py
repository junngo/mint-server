from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser

from gatherer.views import get_company_info


class Command(BaseCommand):
    """
    Get the Company of stock market Info such as name, code, sector.
    """
    help = 'Get the commpany info'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        print("======= Start (co_info) =======")
        get_company_info()
        print("======= End (co_info) =======")
