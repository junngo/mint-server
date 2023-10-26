from django.test import TestCase
from unittest import mock
from . import views


class StockTestCase(TestCase):
    def test_get_company_info(self):
        with mock.patch("gatherer.views.pd.read_html") as read_html:
            views.get_company_info()
            self.assertEqual(read_html.call_count, 1)
