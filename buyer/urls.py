from django.urls import path
from . import views

urlpatterns = [
    path('purchase', views.FarmPurchasedApi.as_view(), name='farm_buyer_purchase'),
]
