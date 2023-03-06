import FinanceDataReader as fdr
import logging
import os
import requests
import json

from datetime import datetime
from .models import Stock, StockPrice, StockMarket


logger = logging.getLogger(__name__)


def get_stock_list(country=StockMarket.KR):
    """
    한국/미국 주식 종목 조회
    """

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


def get_day_stock_price(country=StockMarket.KR):
    """
    오늘의 주식 가격 조회
    """

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


def get_allday_stock_price():
    """
    22년 ~ 현재까지 주식 가격 조회
    """

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


def test_job():
    logger.info("[test_job] 테스트 잡 실행 및 종료")


def create_token(verifier):
    """
    [한국 투자 증권] 통신을 위한 토큰 발행
    """
    headers = {"content-type":"application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
    }
    API = "oauth2/tokenP"
    URL = f"{verifier.config['URL_BASE']}/{API}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    if res.status_code == 200:
        # 현재는 파일로 토큰 관리 (이후에 캐시로 관리 가능)
        access_token = {"authorization": res.json()["access_token"]}
        with open(os.path.join(verifier.root_path, verifier.config['TOKEN_FILE']), 'w') as f:
            json.dump(access_token, f)
        logger.info("[create_token] 토큰 발행 완료 - " + str(res.status_code))
    else:
        logger.info("[create_token] - 토큰 발행 실패 - " + str(res.status_code))
