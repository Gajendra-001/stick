from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.logout_page, name='logout'),
    path('test-dashboard/', views.test_dashboard, name='test-dashboard'),
    
    # Placeholder URLs for other pages (will be moved to respective apps later)
    path('location/', views.placeholder_view, name='location_tracking'),
    path('alerts/', views.placeholder_view, name='alerts_list'),
    path('analytics/', views.placeholder_view, name='analytics_dashboard'),
    
    # API Authentication endpoints
    path('api/register/', views.register, name='api_register'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/logout/', views.logout_view, name='api_logout'),
    path('api/verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    
    # API Profile endpoints
    path('api/profile/', views.profile, name='api_profile'),
    path('api/profile/update/', views.update_profile, name='api_update_profile'),
    path('api/profile/extended/', views.UserProfileView.as_view(), name='extended_profile'),
]
