
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Authentication URLs
    path('auth/', include('rest_framework.urls')),
    # Direct login path
    from django.views.decorators.csrf import csrf_exempt
    from django.utils.decorators import method_decorator
    @method_decorator(csrf_exempt, name='dispatch')
    class LoginView(UserViewSet):
        permission_classes = [permissions.AllowAny]
        def post(self, request):
            return self.login(request)
    path('login/', LoginView.as_view()),
]
