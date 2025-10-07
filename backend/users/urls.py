
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
    path('login/', UserViewSet.as_view({'post': 'login'})),
]
