import os

from django.apps import AppConfig
from django.conf import settings


class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock'
