from datetime import datetime
from django.test import TestCase
from unittest import mock
from . import views

from stock import models
from stock.verifier import Verifier


verifier_config = {
    'APP_KEY': 'app_key',
    'APP_SECRET': 'app_secret_key',
    'CANO': '10074217',
    'ACNT_PRDT_CD': '01',
    'URL_BASE': 'https://test.url.com:29443',
    'TOKEN_FILE': 'token_test.yaml',
    'WORK_ENV': 'test',
    'ROOT_PATH': '/usr/src/app',
    'TOKEN': '/usr/src/token_test.yaml'
}

class StockTestCase(TestCase):

    def setUp(self):
        self.verifier = Verifier()
        self.verifier.config = verifier_config

        self.company = models.Company.objects.create(
            name="삼성전자",
            code="005930",
            sector="반도체",
            public_date="2008-11-13",
            settlement_month="12월",
            region="경기 수원",
        )

    def test_get_company_info(self):
        with mock.patch("gatherer.views.pd.read_html") as read_html:
            views.get_company_info()
            self.assertEqual(read_html.call_count, 1)

    def test_get_stock_price(self):
        with mock.patch("gatherer.views.requests.get") as get, mock.patch(
            "gatherer.views.open"), mock.patch(
            "gatherer.views.json.load"):
            get.return_value.status_code = 200
            get.return_value.json.return_value = {
                "rt_cd": "0",
                "output2": [{
                    "stck_bsop_date": "20231113",
                    "stck_oprc": "70000",
                    "stck_clpr": "72000",
                    "stck_hgpr": "73500",
                    "stck_lwpr": "70000",
                    "acml_vol": "50000000"
                }]
            }

            start_date = datetime.strptime('20231101', '%Y%m%d')
            end_date = datetime.strptime('20231105', '%Y%m%d')
            views.get_stock_price_kis(self.verifier, '005930', start_date, end_date)
            self.assertEqual(get.call_count, 1)

    def test_get_financial_data(self):
        pass
        # verifier = Verifier()
        # verifier.init_load()
        # views.get_financial_data(verifier)
        # views.get_financial_data(verifier, '005930')
