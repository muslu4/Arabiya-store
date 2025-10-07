
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.backends import BaseBackend
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, unique=True, verbose_name="رقم الهاتف")
    address = models.TextField(blank=True, null=True, verbose_name="العنوان")
    is_customer = models.BooleanField(default=True, verbose_name="عميل")
    is_staff_member = models.BooleanField(default=False, verbose_name="موظف")

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"

    def __str__(self):
        return self.username


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None):
        try:
            user = User.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
