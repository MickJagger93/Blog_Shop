from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view,name="cart"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('side_cart/', views.side_cart, name="side_cart_items"),
]