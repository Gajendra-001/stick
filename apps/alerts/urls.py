from django.urls import path
from . import views

urlpatterns = [
    path('alerts/', views.alerts_list, name='alerts_list'),
]