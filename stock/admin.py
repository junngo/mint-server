from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import StockMarket, Stock, StockPrice, Portfolio, PortfolioStock


class PortfolioStockInline(admin.StackedInline):
    model = PortfolioStock
    extra = 3


class PortfolioAdmin(SummernoteModelAdmin):
    inlines = [PortfolioStockInline]
    summernote_fields = ('description',)


admin.site.register(StockMarket)
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(PortfolioStock)
