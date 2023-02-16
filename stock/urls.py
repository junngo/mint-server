from django.urls import path

from . import views

urlpatterns = [
    path("all", views.GetAllStockView.as_view(), name="stocks"),
    path('', views.index, name='index'),
]
