from django.contrib import admin

from .models import StockMarket, Stock, StockPrice, Portfolio, PortfolioStock


class PortfolioStockInline(admin.StackedInline):
    model = PortfolioStock
    extra = 3


class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioStockInline]


admin.site.register(StockMarket)
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(PortfolioStock)
