from django.shortcuts import render
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
]
