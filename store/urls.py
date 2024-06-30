from django.shortcuts import render
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('loginUser', views.loginUser, name="loginUser"),
    path('logoutUser', views.logoutUser, name="logoutUser"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path("update_cart", views.updateCart, name="update_cart"), # for data of cart total qty

    path("user_profile", views.userProfile, name="user_profile")


]
