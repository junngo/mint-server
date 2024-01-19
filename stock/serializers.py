from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'code', 'sector', 'product', 'public_date', 'settlement_month', 'ceo_name', 'homepage', 'region']
