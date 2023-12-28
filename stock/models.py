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


class FinancialState(models.Model):
    """
    Company Financial statement
    """
    REPORT_1YEAR = "11011"
    REPORT_Q1 = "11013"
    REPORT_HALF_YEAR = "11012"
    REPORT_Q3 = "11014"
    REPORT_CHOICES = {
        (REPORT_1YEAR, '1 YEAR'),
        (REPORT_Q1, 'Q1'),
        (REPORT_HALF_YEAR, 'Q2'),
        (REPORT_Q3, 'Q3'),
    }

    DIV_OFS = "OFS"
    DIV_CFS = "CFS"
    FS_DIV_CHOICES = {
        (DIV_OFS, "재무제표"),
        (DIV_CFS, "연결재무제표"),
    }

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="company_financial_state")
    year = models.CharField(max_length=4)
    report = models.CharField(max_length=5, choices=REPORT_CHOICES)
    fs_div = models.CharField(max_length=3, choices=FS_DIV_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BalanceSheet(models.Model):
    """
    재무상태표(자산=부채+자본)
    """
    fs = models.ForeignKey(FinancialState, on_delete=models.PROTECT, related_name="balance_sheet")
    total_assets = models.BigIntegerField(null=True, blank=True)           # 자산총계
    total_liabilities = models.BigIntegerField(null=True, blank=True)      # 부채총계
    total_equity = models.BigIntegerField(null=True, blank=True)           # 자본총계
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IncomeStatement(models.Model):
    """
    손익계산서(수익-비용)
    """
    fs = models.ForeignKey(FinancialState, on_delete=models.PROTECT, related_name="income_statement")
    total_Revenue = models.BigIntegerField(null=True, blank=True)   # 수익(매출액)
    net_income = models.BigIntegerField(null=True, blank=True)      # 당기순이익(손실)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ratios(models.Model):

    fs = models.ForeignKey(FinancialState, on_delete=models.PROTECT, related_name="ratios")
    share_count = models.BigIntegerField(null=True, blank=True)
    preference_share_count = models.BigIntegerField(null=True, blank=True)
    eps = models.IntegerField(null=True, blank=True)
    roe = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
