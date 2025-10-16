
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid


class Coupon(models.Model):
    """نموذج الكوبونات للخصم"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField('كود الكوبون', max_length=20, unique=True)
    description = models.TextField('وصف الكوبون', blank=True)

    # نوع الخصم
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'نسبة مئوية'),
        ('fixed', 'قيمة ثابتة'),
    ]
    discount_type = models.CharField(
        'نوع الخصم',
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage'
    )

    # قيمة الخصم
    discount_value = models.DecimalField(
        'قيمة الخصم',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    # الحد الأدنى للطلب لاستخدام الكوبون
    minimum_order_amount = models.DecimalField(
        'الحد الأدنى للطلب',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    # الحد الأقصى لقيمة الخصم (للكوبونات ذات النسبة المئوية)
    max_discount_amount = models.DecimalField(
        'الحد الأقصى للخصم',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    # تواريخ الصلاحية
    start_date = models.DateTimeField('تاريخ البدء', default=timezone.now)
    end_date = models.DateTimeField('تاريخ الانتهاء')

    # عدد مرات الاستخدام
    usage_limit = models.PositiveIntegerField(
        'حد الاستخدام',
        null=True,
        blank=True,
        help_text='عدد المرات التي يمكن استخدام الكوبون فيها (فارغ للعد غير المحدود)'
    )
    used_count = models.PositiveIntegerField('عدد مرات الاستخدام', default=0)

    # هل الكوبون نشط
    is_active = models.BooleanField('نشط', default=True)

    # المنتجات والأقسام المستثناة - تم تعطيل مؤقتًا لحل مشاكل قاعدة البيانات
    # excluded_products = models.ManyToManyField(
    #     'Product',
    #     related_name='excluded_coupons',
    #     blank=True,
    #     verbose_name='المنتجات المستثناة'
    # )
    # excluded_categories = models.ManyToManyField(
    #     'Category',
    #     related_name='excluded_coupons',
    #     blank=True,
    #     verbose_name='الأقسام المستثناة'
    # )

    # المنتجات والأقسام المحددة (إذا تم تحديدها، يعمل الكوبون عليها فقط) - تم تعطيل مؤقتًا
    # applicable_products = models.ManyToManyField(
    #     'Product',
    #     related_name='applicable_coupons',
    #     blank=True,
    #     verbose_name='المنتجات المحددة'
    # )
    # applicable_categories = models.ManyToManyField(
    #     'Category',
    #     related_name='applicable_coupons',
    #     blank=True,
    #     verbose_name='الأقسام المحددة'
    # )

    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = 'كوبون الخصم'
        verbose_name_plural = 'كوبونات الخصم'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.get_discount_display()}"

    def get_discount_display(self):
        """عرض قيمة الخصم بشكل مناسب"""
        if self.discount_type == 'percentage':
            return f"{self.discount_value}%"
        else:
            return f"{self.discount_value} د.ع"

    def is_valid(self, cart_total=Decimal(0)):
        """التحقق مما إذا كان الكوبون صالحًا للاستخدام"""
        now = timezone.now()

        # التحقق من أن الكوبون نشط
        if not self.is_active:
            return False, "الكوبون غير نشط"

        # التحقق من تاريخ الصلاحية
        if now < self.start_date:
            return False, "الكوبون لم يبدأ بعد"
        if now > self.end_date:
            return False, "انتهت صلاحية الكوبون"

        # التحقق من الحد الأقصى للاستخدام
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "تم الوصول إلى الحد الأقصى لاستخدام هذا الكوبون"

        # التحقق من الحد الأدنى للطلب
        if cart_total < self.minimum_order_amount:
            return False, f"الحد الأدنى للطلب هو {self.minimum_order_amount} د.ع"

        return True, "الكوبون صالح"

    def calculate_discount(self, cart_items, cart_total):
        """حساب قيمة الخصم"""
        is_valid, message = self.is_valid(cart_total)
        if not is_valid:
            return Decimal(0), message

        discount_amount = Decimal(0)
        applicable_items_total = Decimal(0)

        # جمع قيمة العناصر القابلة للتطبيق
        for item in cart_items:
            product = item['product']

            # التحقق من المنتجات المستثناة - تم تعطيل مؤقتًا
            # if self.excluded_products.filter(id=product.id).exists():
            #     continue

            # التحقق من الأقسام المستثناة - تم تعطيل مؤقتًا
            # if self.excluded_categories.filter(id=product.category.id).exists():
            #     continue

            # التحقق من المنتجات المحددة - تم تعطيل مؤقتًا
            # if self.applicable_products.exists() and not self.applicable_products.filter(id=product.id).exists():
            #     continue

            # التحقق من الأقسام المحددة - تم تعطيل مؤقتًا
            # if self.applicable_categories.exists() and not self.applicable_categories.filter(id=product.category.id).exists():
            #     continue

            # إضافة قيمة المنتج إلى المجموع
            applicable_items_total += item['price'] * item['quantity']

        # حساب الخصم
        if self.discount_type == 'percentage':
            discount_amount = applicable_items_total * (self.discount_value / Decimal(100))

            # تطبيق الحد الأقصى للخصم إذا تم تحديده
            if self.max_discount_amount and discount_amount > self.max_discount_amount:
                discount_amount = self.max_discount_amount
        else:
            discount_amount = min(self.discount_value, applicable_items_total)

        return discount_amount, message

    def use_coupon(self):
        """زيادة عدد مرات الاستخدام"""
        self.used_count += 1
        self.save(update_fields=['used_count'])


class CouponUsage(models.Model):
    """تتبع استخدامات الكوبونات"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, verbose_name='الكوبون')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, verbose_name='الطلب')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='المستخدم')
    discount_amount = models.DecimalField('قيمة الخصم', max_digits=10, decimal_places=2)
    used_at = models.DateTimeField('تاريخ الاستخدام', auto_now_add=True)

    class Meta:
        verbose_name = 'استخدام الكوبون'
        verbose_name_plural = 'استخدامات الكوبون'
        ordering = ['-used_at']
        unique_together = ['coupon', 'order']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.coupon.code} - {self.discount_amount} د.ع"
