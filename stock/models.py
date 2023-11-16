from django.db import models


class Company(models.Model):
    """
    Company Model
    """

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=12)
    sector = models.CharField(max_length=100)
    product = models.CharField(null=True, blank=True, max_length=255)
    public_date = models.DateField()
    settlement_month = models.CharField(max_length=10)
    ceo_name = models.CharField(null=True, blank=True, max_length=50)
    homepage = models.CharField(null=True, blank=True, max_length=100)
    region = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class StockPrice(models.Model):
    """
    Stock Price Model
    """

    stock = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="stock_price")
    stock_date = models.DateField()
    open_price = models.IntegerField()
    high_price = models.IntegerField()
    low_price = models.IntegerField()
    close_price = models.IntegerField()
    volume = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
