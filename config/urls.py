"""
URL configuration for Smart Blind Stick project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/devices/', include('apps.devices.urls')),
    path('api/tracking/', include('apps.tracking.urls')),
    path('api/alerts/', include('apps.alerts.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/guardians/', include('apps.guardians.urls')),
    path('', include('apps.users.urls')),  # Include user URLs for main pages
    path('', include('apps.devices.urls')),  # Include device URLs for main pages
    path('', include('apps.tracking.urls')),  # Include tracking URLs for main pages
    path('', include('apps.alerts.urls')),  # Include alerts URLs for main pages
    path('', include('apps.analytics.urls')),  # Include analytics URLs for main pages
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
