from datetime import date
from django.test import TestCase
from unittest import mock

from .models import Company, StockPrice
from .views import create_token, calculate_moving_average
from .verifier import Verifier


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

    def setUp(self) -> None:
        self.verifier = Verifier()
        self.verifier.config = verifier_config

    def test_create_token(self):
        with mock.patch("stock.views.requests.post") as post, mock.patch(
            "stock.views.open") as open, mock.patch(
            "stock.views.json.dump") as dump:
            post.return_value.status_code = 200
            post.return_value.json.return_value = {'access_token': 'token'}

            create_token(self.verifier)

            self.assertEqual(post.call_count, 1)
            self.assertEqual(open.call_count, 1)
            self.assertEqual(dump.call_count, 1)


class MovingAverageTest(TestCase):
    def setUp(self):
        # Create a sample company
        self.company = Company.objects.create(
            name="삼성전자",
            code="005930",
            sector="반도체",
            public_date="2008-11-13",
            settlement_month="12월",
            region="경기 수원",
        )

        # Create sample stock prices for the company
        for i in range(1, 6):
            close_price = 100 + (i * 10)
            StockPrice.objects.create(
                stock=self.company,
                stock_date=date(2024, 1, i),
                open_price=100,
                high_price=100,
                low_price=100,
                close_price=close_price,
                volume=100
            )

    def test_calculate_five_day_moving_average(self):
        # Calculate the 5-day moving average for the most recent date
        result = calculate_moving_average(self.company, reference_date='2024-01-05', period=5)
        self.assertEqual(result, 130)  # Assert the calculated average is as expected

        # Fetch the most recent stock price record
        most_recent_record = StockPrice.objects.filter(stock=self.company).latest('stock_date')

        # Assert the moving average has been saved correctly
        self.assertEqual(most_recent_record.moving_average_5, 130)
