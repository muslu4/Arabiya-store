from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                 'phone', 'address', 'is_customer', 'is_staff_member', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(source='username')
    governorate = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'password_confirm', 'address', 'name', 'governorate']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("كلمتا المرور غير متطابقتين")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        # Extract governorate if present
        governorate = validated_data.pop('governorate', '')

        # Combine name and governorate into address
        address = validated_data.get('address', '')
        if governorate:
            if address:
                address = f"{address}, {governorate}"
            else:
                address = governorate

        validated_data['address'] = address

        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            user = authenticate(username=phone, password=password)

            if not user:
                raise serializers.ValidationError('بيانات الدخول غير صحيحة')

            if not user.is_active:
                raise serializers.ValidationError('حساب المستخدم غير نشط')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('رقم الهاتف وكلمة المرور مطلوبان')
