from django.urls import path
from . import views

urlpatterns = [
    path('location/', views.location_tracking, name='location_tracking'),
]