from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for phone-based authentication"""
    
    def create_user(self, phone, password=None, **extra_fields):
        """Create and return a regular user with phone and password"""
        if not phone:
            raise ValueError('رقم الهاتف مطلوب')
        
        # Normalize phone number (remove spaces, dashes, etc.)
        phone = self.normalize_phone(phone)
        
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, password=None, **extra_fields):
        """Create and return a superuser with phone and password"""
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone, password, **extra_fields)
    
    def normalize_phone(self, phone):
        """Normalize phone number by removing non-digit characters"""
        if not phone:
            return phone
        
        # Special case for admin user
        if phone == 'admin':
            return phone
        
        # Remove all non-digit characters
        normalized = ''.join(filter(str.isdigit, phone))
        
        # Add country code if not present (assuming Saudi Arabia +966)
        if len(normalized) == 9 and normalized.startswith('5'):
            normalized = '966' + normalized
        elif len(normalized) == 10 and normalized.startswith('05'):
            normalized = '966' + normalized[1:]
        
        return normalized


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model with phone-based authentication"""
    
    phone = models.CharField(
        'رقم الهاتف',
        max_length=20,
        unique=True,
        help_text='رقم الهاتف مع رمز البلد (مثال: 966501234567)'
    )
    first_name = models.CharField('الاسم الأول', max_length=30, blank=True)
    last_name = models.CharField('اسم العائلة', max_length=30, blank=True)
    
    is_active = models.BooleanField(
        'نشط',
        default=True,
        help_text='يحدد ما إذا كان هذا المستخدم نشطًا أم لا'
    )
    is_admin = models.BooleanField(
        'مشرف',
        default=False,
        help_text='يحدد ما إذا كان المستخدم مشرفًا'
    )
    
    date_joined = models.DateTimeField('تاريخ الانضمام', default=timezone.now)
    last_login = models.DateTimeField('آخر تسجيل دخول', blank=True, null=True)
    
    # Firebase Cloud Messaging token for push notifications
    device_token = models.TextField(
        'رمز الجهاز',
        blank=True,
        null=True,
        help_text='رمز Firebase للإشعارات'
    )
    
    # Additional user information
    address = models.TextField('العنوان', blank=True)
    city = models.CharField('المدينة', max_length=50, blank=True)
    governorate = models.CharField('المحافظة', max_length=50, blank=True)
    postal_code = models.CharField('الرمز البريدي', max_length=10, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'
        db_table = 'users'
    
    def __str__(self):
        return self.phone
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between"""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name or self.phone
    
    def get_short_name(self):
        """Return the short name for the user"""
        return self.first_name or self.phone
    
    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_admin
    
    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_admin
    
    def save(self, *args, **kwargs):
        """Override save to normalize phone number"""
        if self.phone:
            self.phone = User.objects.normalize_phone(self.phone)
        super().save(*args, **kwargs)


class Notification(models.Model):
    """Simple notification stored in DB"""
    LEVEL_CHOICES = [
        ('info', 'معلومة'),
        ('success', 'نجاح'),
        ('warning', 'تحذير'),
        ('error', 'خطأ'),
    ]

    title = models.CharField('العنوان', max_length=200)
    body = models.TextField('المحتوى', blank=True)
    recipient = models.ForeignKey(
        'users.User',
        verbose_name='المستلم',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='user_notifications'
    )
    level = models.CharField('النوع', max_length=10, choices=LEVEL_CHOICES, default='info')
    is_read = models.BooleanField('مقروء', default=False)
    created_at = models.DateTimeField('تاريخ الإنشاء', default=timezone.now)

    class Meta:
        verbose_name = 'إشعار'
        verbose_name_plural = 'الإشعارات'
        ordering = ['-created_at']

    def __str__(self):
        return self.title