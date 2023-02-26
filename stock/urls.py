from django.urls import path

from . import views

# stock/
urlpatterns = [
    path("all", views.GetAllStockView.as_view(), name="stocks"),
    path("portfolio/<int:portfolio_id>", views.GetPortfolioView.as_view(), name="portfolio"),
    path('', views.index, name='index'),
]
