
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .views import UserViewSet, LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet)

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny



urlpatterns = [
    path('', include(router.urls)),
    # Authentication URLs
    path('auth/', include('rest_framework.urls')),
    # Direct login path
    path('login/', csrf_exempt(LoginView.as_view())),
]
