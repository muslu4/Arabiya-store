from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'phone', 'password', 'password_confirm',
            'first_name', 'last_name', 'address', 'city', 'governorate'
        )
        extra_kwargs = {
            'phone': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("كلمات المرور غير متطابقة")
        return attrs
    
    def validate_phone(self, value):
        """Validate phone number format"""
        if not value:
            raise serializers.ValidationError("رقم الهاتف مطلوب")
        
        # Remove non-digit characters for validation
        digits_only = ''.join(filter(str.isdigit, value))
        
        if len(digits_only) < 9:
            raise serializers.ValidationError("رقم الهاتف قصير جداً")
        
        if len(digits_only) > 15:
            raise serializers.ValidationError("رقم الهاتف طويل جداً")
        
        return value
    
    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    device_token = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Validate user credentials"""
        phone = attrs.get('phone')
        password = attrs.get('password')
        device_token = attrs.get('device_token')
        
        if phone and password:
            # Normalize phone number
            normalized_phone = User.objects.normalize_phone(phone)
            
            user = authenticate(
                request=self.context.get('request'),
                username=normalized_phone,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'رقم الهاتف أو كلمة المرور غير صحيحة'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'هذا الحساب غير نشط'
                )
            
            # Update device token if provided
            if device_token:
                user.device_token = device_token
                user.save(update_fields=['device_token'])
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'رقم الهاتف وكلمة المرور مطلوبان'
            )


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'phone', 'first_name', 'last_name', 'full_name',
            'address', 'city', 'governorate', 'postal_code', 'date_joined', 'is_admin'
        )
        read_only_fields = ('id', 'phone', 'date_joined', 'is_admin')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'address', 'city', 'governorate', 'postal_code'
        )
    
    def validate_first_name(self, value):
        # Optional: allow empty values, but if provided ensure non-empty after trim
        if value is None:
            return value
        if not value.strip():
            raise serializers.ValidationError("الاسم الأول لا يمكن أن يكون فارغاً")
        return value.strip()
    
    def validate_last_name(self, value):
        if value is None:
            return value
        if not value.strip():
            raise serializers.ValidationError("اسم العائلة لا يمكن أن يكون فارغاً")
        return value.strip()


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        min_length=6,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validate password change"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("كلمات المرور الجديدة غير متطابقة")
        return attrs
    
    def validate_old_password(self, value):
        """Validate old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("كلمة المرور الحالية غير صحيحة")
        return value


class DeviceTokenSerializer(serializers.Serializer):
    """Serializer for updating device token"""
    device_token = serializers.CharField(required=True)
    
    def validate_device_token(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("رمز الجهاز مطلوب")
        return value.strip()