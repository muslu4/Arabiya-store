from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.utils import timezone
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    DeviceTokenSerializer
)
from .utils import send_push_to_admins


class UserRegistrationView(APIView):
    """User registration endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Send notification to admins about new user
            try:
                send_push_to_admins(
                    title="مستخدم جديد",
                    body=f"انضم مستخدم جديد: {user.get_full_name()}",
                    data={'type': 'new_user', 'user_id': str(user.id)}
                )
            except Exception as e:
                # Log error but don't fail registration
                print(f"Failed to send admin notification: {e}")
            
            return Response({
                'message': 'تم إنشاء الحساب بنجاح',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'message': 'تم تسجيل الدخول بنجاح',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """Get user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """Update user profile"""
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            response.data = {
                'message': 'تم تحديث الملف الشخصي بنجاح',
                'user': UserProfileSerializer(self.get_object()).data
            }
        return response


class ChangePasswordView(APIView):
    """Change user password"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'تم تغيير كلمة المرور بنجاح'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeviceTokenView(APIView):
    """Update user's device token for push notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = DeviceTokenSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            user.device_token = serializer.validated_data['device_token']
            user.save(update_fields=['device_token'])
            
            return Response({
                'message': 'تم تحديث رمز الجهاز بنجاح'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """User logout endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Clear device token
            user = request.user
            user.device_token = None
            user.save(update_fields=['device_token'])
            
            return Response({
                'message': 'تم تسجيل الخروج بنجاح'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'حدث خطأ أثناء تسجيل الخروج'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user statistics (for admin users)"""
    if not request.user.is_admin:
        return Response({
            'error': 'غير مصرح لك بالوصول لهذه البيانات'
        }, status=status.HTTP_403_FORBIDDEN)
    
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    admin_users = User.objects.filter(is_admin=True).count()
    recent_users = User.objects.filter(
        date_joined__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    
    return Response({
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users,
        'recent_users': recent_users,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_admin_status(request):
    """Check if user is admin"""
    return Response({
        'is_admin': request.user.is_admin,
        'is_superuser': request.user.is_superuser,
    }, status=status.HTTP_200_OK)