import FinanceDataReader as fdr

from django.http import HttpResponse

from .models import Stock, StockPrice


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getStockPrice():
    stocks = Stock.objects.all()
    for stock in stocks:
        df = fdr.DataReader(stock.ticker, '2023-02-02', '2023-02-02')
        for idx, row in df.iterrows():
            StockPrice.objects.create(
                stock_id = stock,
                stock_date = idx,
                open_price = row.get("Open", None),
                high_price = row.get("High", None),
                low_price = row.get("Low", None),
                close_price = row.get("Close", None),
                adj_close_price = row.get("Adj Close", None),
                volume = row.get("Volume", None),
                change = row.get("Change", None),
            )
