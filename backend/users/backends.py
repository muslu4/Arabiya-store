
from django.contrib.auth.backends import BaseBackend
from .models import User
from django.db.models import Q

class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        # تحقق من وجود المستخدم المدير
        if not User.objects.filter(phone='01234567890').exists():
            # إنشاء المستخدم المدير إذا لم يكن موجودًا
            User.objects.create_superuser(
                username='admin',
                phone='01234567890',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("Superuser created successfully!")

        try:
            # البحث عن المستخدم باستخدام رقم الهاتف أو اسم المستخدم
            user = User.objects.get(
                Q(phone=phone) | Q(username=phone)
            )

            # التحقق من كلمة المرور
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
