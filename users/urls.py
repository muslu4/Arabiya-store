from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='profile-update'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # Device token for push notifications
    path('device-token/', views.UpdateDeviceTokenView.as_view(), name='device-token'),
    
    # Admin endpoints
    path('stats/', views.user_stats, name='user-stats'),
    path('check-admin/', views.check_admin_status, name='check-admin'),
]