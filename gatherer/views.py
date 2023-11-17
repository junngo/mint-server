import ast
import json
import pandas as pd
import requests

from datetime import datetime, timedelta
from stock import models
from stock.verifier import Verifier


def get_company_info():
    source_url = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download"
    df_companys = pd.read_html(source_url, header=0)[0]
    for company in df_companys.iterrows():
        data = company[1]
        code = str(data[1])
        stock_code = ('0' * (6-len(code))) + code

        is_company = models.Company.objects.filter(
            code=stock_code).exists()
        if is_company:
            continue

        models.Company.objects.create(
            name=data[0],
            code=stock_code,
            sector=data[2],
            product=data[3],
            public_date=data[4],
            settlement_month=data[5],
            ceo_name=data[6],
            homepage=data[7],
            region=data[8],
        )

def gather_stock_price(start_date, end_date):
    verifier = Verifier()
    verifier.init_load()

    companys = models.Company.objects.all()
    for company in companys:
        get_stock_price_kis(verifier, company.code, start_date, end_date)


def get_stock_price_kis(verifier, code, start_date, end_date):
    """
    [KIS] Get Stock Price from the KIS
    :param verifier: Needed info to call the api (Verifier)
    :param code: stock symbol (e.x, str-005930)
    :param start_date: Start Date (e.x, datetime-2023-11-01)
    :param end_date: End Date (e.x, datetime-2023-11-01)
    """

    with open(verifier.config['TOKEN'], 'r') as f:
        authorization = json.load(f)['authorization']

    API = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{verifier.config['URL_BASE']}{API}"
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {authorization}",
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
        "tr_id": "FHKST03010100",
        "custtype": "P" # 개인:P, 법인:B
    }

    delta = (end_date - start_date).days + 1
    start_date_input = start_date
    DATE_RANGE = 98
    for _ in range(0, delta, DATE_RANGE):
        end_date_input = start_date_input + timedelta(days=DATE_RANGE)
        if end_date < start_date_input:
            break
        elif end_date < end_date_input:
            end_date_input = end_date

        # Get the price from the api result
        query_param = {
            "FID_COND_MRKT_DIV_CODE": "J",  # J: 주식,ETF,ETN
            "FID_INPUT_ISCD": code,         # 종목번호 (6자리)
            "FID_INPUT_DATE_1": start_date_input.strftime("%Y%m%d"),
            "FID_INPUT_DATE_2": end_date_input.strftime("%Y%m%d"),
            "FID_PERIOD_DIV_CODE": "D",     # D:일봉,W:주봉,M:월봉,Y:년봉
            "FID_ORG_ADJ_PRC": "1",         # 0:수정주가, 1:원주가
        }
        response = requests.get(URL, headers=headers, params=query_param)

        if response.status_code == 200 and response.json()["rt_cd"] == '0':
            stocks = response.json()["output2"]
            for stock in stocks:
                company = models.Company.objects.filter(code=code).first()

                date_format = datetime.strptime(stock["stck_bsop_date"], '%Y%m%d')
                is_price = models.StockPrice.objects.filter(
                    stock=company, stock_date=date_format).exists()
                if is_price:
                    continue

                models.StockPrice.objects.create(
                    stock=company,
                    stock_date=date_format,
                    open_price=stock["stck_oprc"],
                    high_price=stock["stck_hgpr"],
                    low_price=stock["stck_lwpr"],
                    close_price=stock["stck_clpr"],
                    volume=stock["acml_vol"],
                )

        start_date_input = end_date_input + timedelta(days=1)


def get_stock_price_naver(code, start_date, end_date):
    """
    [Temporary] - Get Stock Price from the naver
    :code: stock symbol (e.x, 005930)
    :start_date: Start Date (e.x, 20231101)
    :end_date: End Date (e.x, 20231101)
    """
    source_url = f"https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime={start_date}&endTime={end_date}&timeframe=day"
    response = requests.get(source_url)

    data = ast.literal_eval(response.text.strip())
    df_data = pd.DataFrame(data, columns=data[0])

    df_data.drop(0, inplace=True)
    df_data['날짜'] = pd.to_datetime(df_data['날짜'])
    ohlcv = ['시가', '고가', '저가', '종가', '거래량']
    df_data[ohlcv] = df_data[ohlcv].apply(pd.to_numeric)
    for price in df_data.iterrows():
        print(price)


def get_financial_data():
    pass
