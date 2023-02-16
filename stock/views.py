from django.http import HttpResponse
from datetime import date
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class GetAllStockView(APIView):

    def get(self, request):
        """
        주식리스트 조회
        """
        stocks = models.Stock.objects.all()
        serializer = serializers.GetAllStocks(stocks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
