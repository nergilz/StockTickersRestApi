from django.contrib import admin
from django.urls import path
from tickers.views import TickerCreateView, TickerListView, TickerRUDView


urlpatterns = [
    path('tickers/create/', TickerCreateView.as_view()),
    path('tickers/all/', TickerListView.as_view()),
    path('tickers/detail/<int:pk>/', TickerRUDView.as_view())
    ]
