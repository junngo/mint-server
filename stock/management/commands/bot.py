import logging
from django.core.management.base import BaseCommand

import stock.batch_job as jobs
from stock.verifier import Verifier

logger = logging.getLogger("bot")


class Command(BaseCommand):
    help = 'Run the Bot'

    def __init__(self) -> None:
        super().__init__()
        self.verifier = Verifier()

    def add_arguments(self, parser): 
        parser.add_argument('-j' , '--job' , required=True, type=str, help="Job names") 

    def handle(self, *args, **options):
        # 호출 시 인자값 검증 및 config 값 로드
        self.verifier.init_load()
        job = options["job"]

        logger.info(f"[{job}] 배치 실행 시작")
        if job == "create_token":
            # 토큰발행
            jobs.create_token(self.verifier)
        else:
            logger.info("배치 잡 명령어가 존재하지 않습니다.")
            return

        logger.info(f"[{job}] 배치 실행 종료")
