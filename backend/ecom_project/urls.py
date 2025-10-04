"""
URL configuration for ecom_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import home_view, api_info
from .admin import admin_site

urlpatterns = [
    # Home page
    path('', home_view, name='home'),
    path('api/', api_info, name='api_info'),

    # i18n
    path('i18n/', include('django.conf.urls.i18n')),

    # Accounts
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Admin
    path('admin/', admin_site.urls),
    
    # API Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Routes
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/notifications/', include('notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization is now handled in admin.py