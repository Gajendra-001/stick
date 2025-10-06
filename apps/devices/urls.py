from django.urls import path
from . import views

urlpatterns = [
    path('device/', views.device_detail, name='device_detail'),
]