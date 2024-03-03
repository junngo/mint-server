import json
import requests

from django.db.models import Avg
from datetime import datetime
from rest_framework.generics import ListAPIView
from .models import Company, StockPrice
from .serializers import CompanySerializer

def create_token(verifier):
    """
    [KIS API] Create the token to call the api
    """

    API = "/oauth2/tokenP"
    URL = f"{verifier.config['URL_BASE']}{API}"
    headers = {"content-type":"application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
    }
    res = requests.post(URL, headers=headers, data=json.dumps(body))

    if res.status_code == 200:
        access_token = {"authorization": res.json()["access_token"]}
        with open(verifier.config['TOKEN'], 'w') as f:
            json.dump(access_token, f)
        print("[create_token] Success - " + str(res.status_code))
    else:
        print("[create_token] Fail - " + str(res.status_code))


def calculate_moving_average(company, reference_date=None, period=5):
    # If no specific reference date is provided, use the most recent date in the dataset
    if reference_date is None:
        reference_date = StockPrice.objects.filter(stock=company).latest('stock_date').stock_date
    else:
        # Ensure reference_date is a datetime.date object
        if isinstance(reference_date, str):
            reference_date = datetime.strptime(reference_date, '%Y-%m-%d').date()

    # Fetch the last five available trading days' records up to the reference date
    stock_prices = StockPrice.objects.filter(
        stock=company,
        stock_date__lte=reference_date  # Ensure we're looking at dates up to the reference_date
    ).order_by('-stock_date')[:period]

    if len(stock_prices) < period:
        return "Not enough data to calculate the moving average."

    # Calculate the average of close_price for these days
    average_close_price = stock_prices.aggregate(Avg('close_price'))['close_price__avg']

    # Save the calculated average to the most recent StockPrice record
    recent_record = stock_prices[0]
    if period == 5:
        recent_record.moving_average_5 = average_close_price
    elif period == 20:
        recent_record.moving_average_20 = average_close_price
    elif period == 60:
        recent_record.moving_average_60 = average_close_price
    elif period == 120:
        recent_record.moving_average_120 = average_close_price

    recent_record.save()

    return average_close_price


class CompanyListView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
