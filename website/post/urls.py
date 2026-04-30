from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.post, name="post"),
    path('hit-view/<int:pk>/', views.hit_view, name='hit_view'),
]