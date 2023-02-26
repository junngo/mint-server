from django.db import models

# Create your models here.
class StockMarket(models.Model):
    """
    Stock Market (e.x, Nasdaq)
    """
    name = models.CharField(max_length=20)
    summary = models.CharField(max_length=20)
    country = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.summary}({self.country})"


class Stock(models.Model):
    """
    Stock Model
    """

    ticker = models.CharField(max_length=20)
    ticker_name = models.CharField(max_length=100)
    stock_maket = models.ForeignKey(StockMarket, on_delete=models.PROTECT, related_name="stock", null=True, blank=True)

    def __str__(self) -> str:
        return self.ticker


class StockPrice(models.Model):
    """
    Stock Price Model
    """

    class Meta:
        indexes = [
            models.Index(fields=['stock_id', 'stock_date']),
        ]

    stock_id = models.ForeignKey(Stock, on_delete=models.PROTECT, related_name="stock_price")
    stock_date = models.DateTimeField()
    open_price = models.DecimalField(max_digits=14, decimal_places=6, default=None, blank=True, null=True)
    high_price = models.DecimalField(max_digits=14, decimal_places=6, default=None, blank=True, null=True)
    low_price = models.DecimalField(max_digits=14, decimal_places=6, default=None, blank=True, null=True)
    close_price = models.DecimalField(max_digits=14, decimal_places=6, default=None, blank=True, null=True)
    adj_close_price = models.DecimalField(max_digits=14, decimal_places=6, default=None, blank=True, null=True)
    volume = models.IntegerField(default=None, blank=True, null=True)
    change = models.DecimalField(max_digits=14, decimal_places=6, default=None, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.stock_id.ticker}: {self.stock_date}"


class Portfolio(models.Model):
    """
    Portfolio
    """
    YEAR = 'Y'
    MONTH = 'M'
    DAY = 'D'
    PEROID_UNIT = [
        (YEAR, "Year"),
        (MONTH, "Month"),
        (DAY, "Day"),
    ]
    name = models.CharField(max_length=50)
    description = models.TextField()
    period_unit = models.CharField(max_length=1, choices=PEROID_UNIT, null=True, blank=True)
    rebalancing_period = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class PortfolioStock(models.Model):
    """
    Portfolio Stock
    (One to One relation with the Stock Model)
    """

    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT, related_name="portfolio")
    stock = models.OneToOneField(Stock, on_delete=models.PROTECT)
    ratio = models.IntegerField()
    description = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.portfolio.name} - {self.stock.ticker}"
