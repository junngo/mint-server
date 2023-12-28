import ast
import json
import pandas as pd
import requests
import time
import xml.etree.ElementTree as et

from zipfile import ZipFile
from io import BytesIO
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
        time.sleep(0.05)
        response = requests.get(URL, headers=headers, params=query_param)

        if response.status_code == 200 and response.json()["rt_cd"] == '0':
            stocks = response.json()["output2"]
            for stock in stocks:
                if not stock:
                    continue
                company = models.Company.objects.filter(code=code).first()

                date_format = datetime.strptime(stock["stck_bsop_date"], '%Y%m%d')

                models.StockPrice.objects.update_or_create(
                    stock=company,
                    stock_date=date_format,
                    defaults={
                        "stock": company,
                        "stock_date": date_format,
                        "open_price": stock["stck_oprc"],
                        "high_price": stock["stck_hgpr"],
                        "low_price": stock["stck_lwpr"],
                        "close_price": stock["stck_clpr"],
                        "volume": stock["acml_vol"],
                    }
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


def get_dart_corp_code(verifier):
    """
    [DART] Get that corp code for the DART. Dart has unique corp id.
    :param verifier: Needed info to call the api (Verifier)
    :return: dart code formed DataFrame format
    """
    access_key = verifier.config['DART_KEY']
    URL = "https://opendart.fss.or.kr/api/corpCode.xml"
    query_param = {
        "crtfc_key": access_key
    }
    time.sleep(0.05)
    response = requests.get(URL, params=query_param)
    zipfile = ZipFile(BytesIO(response.content))
    xmlfile = {name: zipfile.read(name) for name in zipfile.namelist()}

    """
    xml example)
    </result>
        <list>
            <corp_code>00126380</corp_code>
            <corp_name>삼성전자</corp_name>
            <stock_code>005930</stock_code>
            <modify_date>20230110</modify_date>
        </list>
        <list>
            <corp_code>01615845</corp_code>
            <corp_name>메타버스월드</corp_name>
            <stock_code> </stock_code>
            <modify_date>20230228</modify_date>
        </list>
    </result>
    """
    xml_str = xmlfile['CORPCODE.xml'].decode('utf-8')
    xml_result = et.fromstring(xml_str)

    df_cols = ["corp_code", "corp_name", "stock_code", "modify_date"]
    corp_data = []
    for xml_list in xml_result:
        row = {}
        for col_name in df_cols:
            value = xml_list.find(col_name).text.strip()
            if not value:
                value = None

            row[col_name] = value
        corp_data.append(row)

    df = pd.DataFrame(corp_data, columns=df_cols)

    return df


def gather_financial_data(start_date, end_date):
    verifier = Verifier()
    verifier.init_load()

    companys = models.Company.objects.all()
    # companys = models.Company.objects.filter(code="005930")
    dart_code = get_dart_corp_code(verifier)

    for company in companys:
        get_financial_data(
            verifier
            , company
            , dart_code
            , '2022'
            , models.FinancialState.REPORT_1YEAR
            , models.FinancialState.DIV_CFS
        )


def get_financial_data(verifier, company, dart_code_all, year, report_code, fs_div):
    """
    [DART] Get Stock financial data from the DART
    :param verifier: Needed info to call the api (Verifier)
    :param code: stock symbol (e.x, str-005930)
    :param start_year: Start year (e.x, str-2023)
    :param end_year: End year (e.x, str-2023)
    :param report_kind: Repor Kind as 1year, 1Q (e.x, datetime-2023)
    """
    access_key = verifier.config['DART_KEY']
    needed_cols = [
        "ifrs-full_Revenue",    # 수익(매출액)
        "ifrs-full_ProfitLoss", # 당기순이익
        "보통주",
        "우선주",
    ]
    dart_code = dart_code_all[dart_code_all['stock_code'] == company.code].iloc[0].corp_code
    fina_data = {}

    # Income Data
    URL = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
    query_param = {
        "crtfc_key": access_key,
        "corp_code": dart_code,
        "bsns_year": year,
        "reprt_code": report_code,  # REPORT_CHOICES
        "fs_div": fs_div,           # OFS:재무제표, CFS:연결재무제표
    }
    time.sleep(0.7)
    response = requests.get(URL, params=query_param)

    # status: 013, message: 조회된 데이타가 없습니다.
    if response.json()["status"] == "013":
        return

    if response.status_code == 200 and response.json()["status"] == "000":
        fs, _ = models.FinancialState.objects.update_or_create(
            company=company,
            year=year,
            report=report_code,
            fs_div=fs_div,
            defaults={
                "company": company,
                "year": year,
                "report": report_code,
                "fs_div": fs_div
            }
        )

        data_list = response.json()["list"]
        for data in data_list:
            if data["account_id"] in needed_cols and data["sj_div"] == "CIS":
            # CIS: 포괄손익계산서
                fina_data[data["account_id"]] = int(data["thstrm_amount"])

        models.IncomeStatement.objects.update_or_create(
            fs=fs,
            defaults={
                "total_Revenue": fina_data.get("ifrs-full_Revenue", None),
                "net_income": fina_data.get("ifrs-full_ProfitLoss", None),
            }
        )

    # Share Count
    # URL = "https://opendart.fss.or.kr/api/stockTotqySttus.json"
    # query_param = {
    #     "crtfc_key": access_key,
    #     "corp_code": dart_code,
    #     "bsns_year": year,
    #     "reprt_code": report_code,
    # }
    # time.sleep(0.7)
    # response = requests.get(URL, params=query_param)
    # if response.status_code == 200 and response.json()["status"] == "000":
    #     data_list = response.json()["list"]
    #     for data in data_list:
    #         if data["se"] in needed_cols and data["istc_totqy"] != "-":
    #             fina_data[data["se"]] = int(data["istc_totqy"].replace(",", ""))

    #     # eps = None
    #     # if fina_data["ifrs-full_ProfitLoss"]:
    #     #     eps = round(fina_data["ifrs-full_ProfitLoss"] / (fina_data.get("보통주", 0) + fina_data.get("우선주", 0)))

    #     models.Ratios.objects.update_or_create(
    #         fs=fs,
    #         defaults={
    #             "share_count": fina_data.get("보통주", None),
    #             "preference_share_count": fina_data.get("우선주", None),
    #             # "eps": eps,
    #         }
    #     )
