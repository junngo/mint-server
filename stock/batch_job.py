import FinanceDataReader as fdr
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .models import Stock, StockPrice


logger = logging.getLogger(__name__)


def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    # @scheduler.scheduled_job('cron', minute="10", name='get_stock_price')
    def register_get_stock_price():
        get_stock_price()
    
    scheduler.start()

def get_stock_price():
    """
    Get Stock Price by batch job
    """
    print("Start getStockPrice()")

    stocks = Stock.objects.all()
    for stock in stocks:
        df = fdr.DataReader(stock.ticker, '2023')
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

    print("End getStockPrice()")
