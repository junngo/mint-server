from django.contrib import admin
from .models import Company, StockPrice, FinancialState, IncomeStatement


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sector', 'product', 'public_date')
    search_fields = ('name', 'code', 'sector',)


class StockPriceAdmin(admin.ModelAdmin):
    list_display = (
        'stock',
        'stock_date',
        'open_price',
        'close_price',
        'volume',
        'moving_average_5',
        'moving_average_20',
        'moving_average_60',
        'moving_average_120',
        'eps',
        'per',
        'pbr',
        'share_count'
    )
    search_fields = ('stock__name', 'stock__code',)


class IncomeStatementInline(admin.TabularInline):
    model = IncomeStatement


class FinancialStateAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', 'report', 'fs_div',)
    search_fields = ('company__name', 'company__code',)

    inlines = [
        IncomeStatementInline,
    ]


admin.site.register(Company, CompanyAdmin)
admin.site.register(StockPrice, StockPriceAdmin)
admin.site.register(FinancialState, FinancialStateAdmin)
