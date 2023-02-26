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
        start_date = now - timedelta(days=10)
        end_date = now
        stock_price = models.StockPrice.objects.filter(
            stock_id=obj.id, 
            stock_date__range=(start_date, end_date)
        )
        serializer = StockPrice(stock_price, many=True, read_only=True)
        return serializer.data


class GetPortfolioStock(serializers.ModelSerializer):
    """
    포트폴리오 주식 <--> 주식은 1:1
    """
    
    stock = GetAllStocks()

    class Meta:
        model = models.PortfolioStock
        fields= ["ratio", "description", "stock"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        stock = representation.pop("stock")
        for key in stock:
            representation[key] = stock[key]
        return representation


class GetPortfolio(serializers.ModelSerializer):
    """
    포트폴리오 설명 with 주식, 주식 가격
    """

    rebalancing_period_unit = serializers.SerializerMethodField()
    stocks = serializers.SerializerMethodField()

    class Meta:
        model = models.Portfolio
        fields = [
            "name",
            "description",
            "rebalancing_period_unit",
            "stocks"
        ]

    def get_rebalancing_period_unit(self, obj):
        return f"{str(obj.rebalancing_period)} {obj.get_period_unit_display()}"

    def get_stocks(self, obj):
        """
        포트폴리오에 포함된 주식&주식가격 조회
        """
        stocks = models.PortfolioStock.objects.filter(portfolio_id=obj.id)
        serializer = GetPortfolioStock(stocks, many=True)
        return serializer.data
