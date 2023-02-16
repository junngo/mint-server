from datetime import datetime, timedelta
from rest_framework import serializers

from . import models


class StockPrice(serializers.ModelSerializer):
    """
    주식 가격 데이터(메인)
    """
    stock_date = serializers.SerializerMethodField()

    class Meta:
        model = models.StockPrice
        fields = "__all__"

    def get_stock_date(self, obj):
        """
        DateTime(2022-10-04 00:00:00) -> Date(2022-10-04) 변환
        """
        return obj.stock_date.date()


class GetAllStocks(serializers.ModelSerializer):
    """
    종류별 주식 데이터(메인)
    """

    stock_price = serializers.SerializerMethodField()

    class Meta:
        model = models.Stock
        fields = ["ticker", "ticker_name", "stock_price"]

    def get_stock_price(self, obj):
        """
        1년 전 ~ 현재까지 기준으로 추출
        """
        now = datetime.now()
        start_date = now - timedelta(days=366)
        end_date = now
        stock_price = models.StockPrice.objects.filter(
            stock_id=obj.id, 
            stock_date__range=(start_date, end_date)
        )
        serializer = StockPrice(stock_price, many=True, read_only=True)
        return serializer.data
