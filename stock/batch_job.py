import FinanceDataReader as fdr
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .models import Stock, StockPrice, StockMarket


logger = logging.getLogger(__name__)


def start():
    scheduler=BackgroundScheduler(timezone='Asia/Seoul')
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    # register_events(scheduler)

    @scheduler.scheduled_job(
        'cron',
        minute="30",
        hour="1",
        max_instances=1,
        name='get_stock_list_kr'
    )
    def register_get_stock_list_kr():
        get_stock_list_kr()


    @scheduler.scheduled_job('cron', minute="33", hour="16", max_instances=1, name='get_stock_price')
    def register_get_stock_price():
        get_stock_price()
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()

def get_stock_list_kr():
    """
    주식 종목 조회 (존재하지 않는 경우만 입력)
    """
    stock_markets = StockMarket.objects.filter(country="KR")
    for stock_market in stock_markets:
        df = fdr.StockListing(stock_market.name)
        for _, row in df[0:1].iterrows():
            stock_market = StockMarket.objects.filter(name__in = row.get("Market", None).split()).first()
            Stock.objects.get_or_create(
                ticker= row.get("Code", None),
                ticker_name = row.get("Name", None),
                stock_market = stock_market
            )

def get_stock_price():
    """
    Get Stock Price by batch job
    """
    stocks = Stock.objects.all()
    for stock in stocks:
        df = fdr.DataReader(stock.ticker, '2020')
        for idx, row in df.iterrows():
            StockPrice.objects.create(
                stock_id = stock,
                stock_date = idx,
                open_price = row.get("Open", None),
                high_price = row.get("High", None),
                low_price = row.get("Low", None),
                close_price = row.get("Close", None),
                adj_close_price = row.get("Adj Close", None),
                volume = row.get("Volume", None),
                change = row.get("Change", None),
            )
