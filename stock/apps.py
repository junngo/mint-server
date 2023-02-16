import os

from django.apps import AppConfig
from django.conf import settings


class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock'

    def ready(self):
        """
        로컬 작업 시 reload로 인해 2번 실행되어, 배치 잡 2번 실행되는 이슈 존재
        RUN_MAIN 분기를 통해서 배치 작업 1번만 실행될 수 있도록 분기 처리
        """
        if os.environ.get('RUN_MAIN', None) != 'true' and settings.SCHEDULER_DEFAULT:
            from . import batch_job
            batch_job.start()
