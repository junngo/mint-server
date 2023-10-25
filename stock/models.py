from django.db import models

# Create your models here.
class Company(models.Model):

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
