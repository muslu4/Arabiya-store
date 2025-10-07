
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        return UserViewSet().login(request)

urlpatterns = [
    path('', include(router.urls)),
    # Authentication URLs
    path('auth/', include('rest_framework.urls')),
    # Direct login path
    path('login/', LoginView.as_view()),
]
