from django.urls import path
from . import views

urlpatterns = [
    path('', views.GuardianRelationListView.as_view(), name='guardian-relation-list'),
    path('dashboard/', views.guardian_dashboard, name='guardian-dashboard'),
    path('dashboard/config/', views.GuardianDashboardView.as_view(), name='guardian-dashboard-config'),
    path('monitoring/<int:user_id>/', views.monitored_user_detail, name='monitored-user-detail'),
    path('notifications/', views.GuardianNotificationListView.as_view(), name='guardian-notification-list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('activities/', views.GuardianActivityListView.as_view(), name='guardian-activity-list'),
    path('send-message/<int:user_id>/', views.send_message_to_user, name='send-message'),
    path('<int:pk>/', views.GuardianRelationDetailView.as_view(), name='guardian-relation-detail'),
]
