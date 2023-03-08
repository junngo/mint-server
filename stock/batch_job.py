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

    API = "/oauth2/tokenP"
    URL = f"{verifier.config['URL_BASE']}{API}"
    headers = {"content-type":"application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
    }
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    if res.status_code == 200:
        # 현재는 파일로 토큰 관리 (이후에 캐시로 관리 가능)
        access_token = {"authorization": res.json()["access_token"]}
        with open(os.path.join(verifier.root_path, verifier.config['TOKEN_FILE']), 'w') as f:
            json.dump(access_token, f)
        logger.info("[create_token] 토큰 발행 완료 - " + str(res.status_code))
    else:
        logger.info("[create_token] 토큰 발행 실패 - " + str(res.status_code))


def get_current_price(verifier, tr_id="005930"):
    """
    [한국 투자 증권] 현재가 시세 조회
    """

    with open(os.path.join(verifier.root_path, verifier.config['TOKEN_FILE']), 'r') as f:
        authorization = json.load(f)['authorization']

    API = "/uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{verifier.config['URL_BASE']}{API}"
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {authorization}",
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
        "tr_id": "FHKST01010100",
        "custtype": "P" # 개인: P, 법인: B
    }
    query_param = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": tr_id, # 삼성전자
    }
    response = requests.get(URL, headers=headers, params=query_param)
    return response


def hashkey(verifier, datas):
    PATH = "/uapi/hashkey"
    URL = f"{verifier.config['URL_BASE']}{PATH}"
    headers = {
        'content-Type' : 'application/json',
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]

    return hashkey


def order_stock(verifier, tr_flag):
    """
    매수/매도 주문
    https://wikidocs.net/159341
    https://apiportal.koreainvestment.com/apiservice/apiservice-domestic-stock#L_aade4c72-5fb7-418a-9ff2-254b4d5f0ceb
    """

    # tr_id 탐색
    if tr_flag == "BUY":
        # 주식 현금 매수 주문
        if verifier.config["WORK_ENV"] == "test":
            tr_id = "VTTC0802U"     # 모의
        elif verifier.config["WORK_ENV"] == "prod":
            tr_id = "TTTC0802U"     # 실전
    elif tr_flag == "SELL":
        # 주식 현금 매도 주문
        if verifier.config["WORK_ENV"] == "test":
            tr_id = "VTTC0801U"     # 모의
        elif verifier.config["WORK_ENV"] == "prod":
            tr_id = "TTTC0801U"     # 실전
    else:
        logger.info("[order_stock] 매수/매도 플래그가 잘못되었습니다.")
        return

    with open(os.path.join(verifier.root_path, verifier.config['TOKEN_FILE']), 'r') as f:
        authorization = json.load(f)['authorization']

    API = "/uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{verifier.config['URL_BASE']}{API}"
    body = {
        "CANO": verifier.config["CANO"],                    # 종합계좌번호
        "ACNT_PRDT_CD": verifier.config["ACNT_PRDT_CD"],    # 계좌상품코드
        "PDNO": "005930",                                   # 종목코드
        "ORD_DVSN": "01",                                   # 주문구분-01:지정가, 02:시장가
        "ORD_QTY": "10",                                    # 주문 주식수
        "ORD_UNPR": "60100",                                # 1주당 가격
    }
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {authorization}",
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
        "tr_id": tr_id,
        "custtype": "P",            # 개인: P, 법인: B
        "hashkey": hashkey(verifier, body)
    }
    response = requests.post(URL, headers=headers, data=json.dumps(body))
    return response


def get_balance(verifier):
    """
    [한국 투자 증권] 주식 잔고 조회
    """

    with open(os.path.join(verifier.root_path, verifier.config['TOKEN_FILE']), 'r') as f:
        authorization = json.load(f)['authorization']

    # 주식 잔고 조회
    if verifier.config["WORK_ENV"] == "test":
        tr_id = "VTTC8434R"     # 모의
    elif verifier.config["WORK_ENV"] == "prod":
        tr_id = "TTTC8434R"     # 실전

    API = "/uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{verifier.config['URL_BASE']}{API}"
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {authorization}",
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
        "tr_id": tr_id,
        "custtype": "P" # 개인: P, 법인: B
    }
    query_param = {
        "CANO": verifier.config["CANO"],                    # 종합계좌번호
        "ACNT_PRDT_CD": verifier.config["ACNT_PRDT_CD"],    # 계좌상품코드
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "01",                                  # 01:대출일별, 02:종목별
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "Y",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "00",                                  # 00:전일매매포함, 01:전일매매미포함
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
    }
    response = requests.get(URL, headers=headers, params=query_param)
    return response
