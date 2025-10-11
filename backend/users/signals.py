from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    """
    إنشاء مستخدم مدير بعد اكتمال الترحيلات
    """
    if sender.name == 'users':
        if not User.objects.filter(phone='01234567890').exists():
            User.objects.create_superuser(
                username='admin',
                phone='01234567890',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("Superuser created successfully!")
