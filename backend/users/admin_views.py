from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

User = get_user_model()

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # تحقق من وجود المستخدم المدير
        if not User.objects.filter(phone='01234567890').exists():
            # إنشاء المستخدم المدير إذا لم يكن موجودًا
            User.objects.create_superuser(
                phone='01234567890',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("Superuser created successfully!")

        # استدعاء الطريقة الأصلية
        return super().form_valid(form)

# تسجيل عرض تسجيل الدخول المخصص
admin.site.login = CustomLoginView.as_view()
