from django.test import TestCase
from stock.models import Stock, StockPrice
from stock.batch_job import get_stock_price

# Create your tests here.
class StockTestCase(TestCase):

    def setUp(self) -> None:
        # Stock.objects.create(ticker="005930", ticker_name="삼성전자")
        # Stock.objects.create(ticker="066570", ticker_name="lg전자")
        Stock.objects.create(ticker="SPY", ticker_name="SPDR S&P 500 ETF")
        Stock.objects.create(ticker="EFA", ticker_name="EFA")


    def test_my_test(self):
        # when-given
        get_stock_price()

        # then
        stockPrice = StockPrice.objects.all()
        self.assertEqual(2, stockPrice.count())
