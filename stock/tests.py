from django.test import TestCase
from stock.models import Stock, StockPrice

from . import batch_job
from .verifier import Verifier


# Create your tests here.
class StockTestCase(TestCase):

    def setUp(self) -> None:
        # Stock.objects.create(ticker="005930", ticker_name="삼성전자")
        # Stock.objects.create(ticker="066570", ticker_name="lg전자")
        # Stock.objects.create(ticker="SPY", ticker_name="SPDR S&P 500 ETF")
        # Stock.objects.create(ticker="EFA", ticker_name="EFA")
        self.verifier = Verifier()
        self.verifier.init_load()


    # def test_my_test(self):
    #     self.assertEqual(True, True)

    # def test_get_current_price(self):
    #     response = batch_job.get_current_price(self.verifier)
    #     print(response.json()['output']['stck_prpr'])
    #     self.assertEqual(response.status_code, 200)

    # def test_get_balance(self):
    #     response = batch_job.get_balance(self.verifier)
    #     print(response.json())
    #     self.assertEqual(False)

    # def test_order_buy_stock(self):
    #     response = batch_job.order_stock(self.verifier, "SELL")
    #     print(response.json())
    #     self.assertEqual(False)