from django.db import models

# Create your models here.
class Stock(models.Model):
    """
    Stock Model
    """

    ticker = models.CharField(max_length=20)
    ticker_name = models.CharField(max_length=20)


class StockPrice(models.Model):
    """
    Stock Price Model
    """

    stock_id = models.ForeignKey(Stock, on_delete=models.SET_NULL)
    stock_date = models.DateField()
    open_price = models.DecimalField(max_digits=8, decimal_places=6, default=None, blank=True, null=True)
    high_price = models.DecimalField(max_digits=8, decimal_places=6, default=None, blank=True, null=True)
    low_price = models.DecimalField(max_digits=8, decimal_places=6, default=None, blank=True, null=True)
    close_price = models.DecimalField(max_digits=8, decimal_places=6, default=None, blank=True, null=True)
    adj_close_price = models.DecimalField(max_digits=8, decimal_places=6, default=None, blank=True, null=True)
    volume = models.IntegerField(default=None, blank=True, null=True)
    change = models.DecimalField(max_digits=8, decimal_places=6, default=None, blank=True, null=True)
