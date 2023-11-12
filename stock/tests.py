from django.test import TestCase
from unittest import mock

from .views import create_token
from .verifier import Verifier


verifier_config = {
    'APP_KEY': 'app_key', 
    'APP_SECRET': 'app_secret_key',
    'CANO': '50078816',
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
