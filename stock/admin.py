from django.contrib import admin
from .models import Company, StockPrice


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sector', 'product', 'public_date')
    search_fields = ('name', 'code', 'sector',)


class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('stock', 'stock_date', 'open_price', 'close_price', 'volume',)
    search_fields = ('stock__name', 'stock__code',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(StockPrice, StockPriceAdmin)
