from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.checkout,name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('mis-compras/', views.mis_compras, name='mis_compras'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('payment_method/', views.payment_method, name='payment_method'),
    path('bank_trasnfer/', views.bank_transfer, name='bank_transfer'),
    path('stripe_payment/', views.stripe_payment, name='stripe_payment'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('create_payment/', views.create_payment, name='create_payment'),
]