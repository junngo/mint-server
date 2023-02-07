import FinanceDataReader as fdr

from django.http import HttpResponse

from .models import Stock, StockPrice


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
