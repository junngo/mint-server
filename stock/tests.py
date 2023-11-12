from django.test import TestCase
from unittest import mock

from .views import create_token
from .verifier import Verifier


# Create your tests here.
class StockTestCase(TestCase):

    def setUp(self) -> None:
        self.verifier = Verifier()
        self.verifier.init_load()

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
