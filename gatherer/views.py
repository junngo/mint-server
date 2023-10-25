import pandas as pd
from stock import models


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

def get_financial_data():
    pass
