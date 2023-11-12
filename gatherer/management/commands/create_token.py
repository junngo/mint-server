from typing import Any, Optional
from django.core.management.base import BaseCommand

from stock.views import create_token
from stock.verifier import Verifier


class Command(BaseCommand):
    """
    [KIS] Get the token from the KIS to access the API
    """
    help = 'Get the token from KIS'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        verifier = Verifier()
        verifier.init_load()

        print("======= Start (create_token) =======")
        create_token(verifier)
        print("======= End (create_token) =======")
