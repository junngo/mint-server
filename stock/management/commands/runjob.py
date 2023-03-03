import datetime
import logging

from django.core.management.base import BaseCommand

import stock.batch_job as jobs

logger = logging.getLogger(__name__)


class Command(BaseCommand): 
    help = 'Show post list'

    def add_arguments(self, parser): 
        parser.add_argument('-j' , '--job' , required=True, type=str, help="Job names") 
        parser.add_argument('-d' , '--date', required=False, type=str)

    def handle(self, *args, **options):
        job = options["job"]
        date = options["date"]
        if date:
            try:
                datetime.date.fromisoformat(date)
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")

        if job == "stock_list_kr":
            # 국내 종목 리스트
            jobs.get_stock_list("KR")
        elif job == "stock_list_us":
            # 해외 종목 리스트
            jobs.get_stock_list("US")
        elif job == "stock_day_price_kr":
            # 국내 일 주식 가격 조회
            jobs.get_day_stock_price("KR")
        elif job == "stock_day_price_us":
            # 해외 일 주식 가격 조회
            jobs.get_day_stock_price("US")
        elif job == "stock_allday_price":
            # 21년 ~ 현재까지 주식 가격 조회
            jobs.get_allday_stock_price()
        elif job == "test_job":
            jobs.test_job()
        else:
            logger.info("배치 잡 명령어가 존재하지 않습니다.")            
