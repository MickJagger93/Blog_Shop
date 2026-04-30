from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clean_history/', views.clean_history, name='clean_history'),
    path('register_clic/', views.register_clic, name='register_clic'),
]
