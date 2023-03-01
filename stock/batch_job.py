import FinanceDataReader as fdr
import logging

from datetime import datetime
from .models import Stock, StockPrice, StockMarket


logger = logging.getLogger(__name__)


def get_stock_list(country=StockMarket.KR):
    """
    한국/미국 주식 종목 조회
    """
    logger.info("[get_stock_list] 시작")
    if country == StockMarket.KR:
        TICKER_LABEL = "Code"
    elif country == StockMarket.US:
        TICKER_LABEL = "Symbol"
    else:
        raise ValueError("[get_stock_list]-country 추가 필요, country: "+ country)
    NAME = "Name"

    stock_markets = StockMarket.objects.filter(country=country)
    for stock_market in stock_markets:
        df = fdr.StockListing(stock_market.name)
        for _, row in df.iterrows():
            Stock.objects.get_or_create(
                ticker= row.get(TICKER_LABEL, None),
                ticker_name = row.get(NAME, None),
                stock_market = stock_market
            )
    logger.info("[get_stock_list] 종료")


def get_day_stock_price(country=StockMarket.KR):
    """
    오늘의 주식 가격 조회
    """
    logger.info("[get_day_stock_price] 시작")
    today = datetime.today().strftime('%Y-%m-%d')
    stocks = Stock.objects.filter(stock_market__country=country)
    for stock in stocks:
        df = fdr.DataReader(stock.ticker, today, today)
        for idx, row in df.iterrows():
            is_stock_price = StockPrice.objects.filter(
                stock=stock, stock_date=idx).exists()
            if is_stock_price:
                continue

            StockPrice.objects.create(
                stock = stock,
                stock_date = idx,
                open_price = row.get("Open", None),
                high_price = row.get("High", None),
                low_price = row.get("Low", None),
                close_price = row.get("Close", None),
                adj_close_price = row.get("Adj Close", None),
                volume = row.get("Volume", None),
                change = row.get("Change", None),
            )
    logger.info("[get_day_stock_price] 종료")


def get_allday_stock_price():
    """
    22년 ~ 현재까지 주식 가격 조회
    """
    logger.info("[get_allday_stock_price] 시작")
    stocks = Stock.objects.all()
    for stock in stocks:
        df = fdr.DataReader(stock.ticker, '2022')
        for idx, row in df.iterrows():
            is_stock_price = StockPrice.objects.filter(
                stock=stock, stock_date=idx).exists()
            if is_stock_price:
                continue

            StockPrice.objects.create(
                stock = stock,
                stock_date = idx,
                open_price = row.get("Open", None),
                high_price = row.get("High", None),
                low_price = row.get("Low", None),
                close_price = row.get("Close", None),
                adj_close_price = row.get("Adj Close", None),
                volume = row.get("Volume", None),
                change = row.get("Change", None),
            )
    logger.info("[get_allday_stock_price] 종료")
