from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class Order(models.Model):
    """Order model"""
    
    STATUS_CHOICES = [
        ('pending', 'في الانتظار'),
        ('confirmed', 'مؤكد'),
        ('processing', 'قيد التحضير'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('cancelled', 'ملغي'),
        ('returned', 'مرتجع'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'في الانتظار'),
        ('paid', 'مدفوع'),
        ('failed', 'فشل الدفع'),
        ('refunded', 'مسترد'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'الدفع عند الاستلام'),
        ('card', 'بطاقة ائتمان'),
        ('bank_transfer', 'تحويل بنكي'),
        ('wallet', 'محفظة إلكترونية'),
    ]
    
    # Order identification
    order_number = models.CharField('رقم الطلب', max_length=20, unique=True)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='المستخدم'
    )
    
    # Order status
    status = models.CharField(
        'حالة الطلب',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_status = models.CharField(
        'حالة الدفع',
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    payment_method = models.CharField(
        'طريقة الدفع',
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash'
    )
    
    # Pricing
    subtotal = models.DecimalField(
        'المجموع الفرعي',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    discount_amount = models.DecimalField(
        'مبلغ الخصم',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    shipping_cost = models.DecimalField(
        'تكلفة الشحن',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    tax_amount = models.DecimalField(
        'مبلغ الضريبة',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    total_amount = models.DecimalField(
        'المبلغ الإجمالي',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Shipping information
    shipping_name = models.CharField('اسم المستلم', max_length=100)
    shipping_phone = models.CharField('هاتف المستلم', max_length=20)
    shipping_address = models.TextField('عنوان الشحن')
    shipping_city = models.CharField('المدينة', max_length=50)
    shipping_postal_code = models.CharField('الرمز البريدي', max_length=10, blank=True)
    
    # Additional information
    notes = models.TextField('ملاحظات', blank=True)
    admin_notes = models.TextField('ملاحظات الإدارة', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    confirmed_at = models.DateTimeField('تاريخ التأكيد', blank=True, null=True)
    shipped_at = models.DateTimeField('تاريخ الشحن', blank=True, null=True)
    delivered_at = models.DateTimeField('تاريخ التسليم', blank=True, null=True)
    
    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['order_number']),
        ]
    
    def __str__(self):
        return f'طلب #{self.order_number} - {self.user.get_full_name()}'
    
    def save(self, *args, **kwargs):
        """Override save to generate order number and calculate total"""
        if not self.order_number:
            self.order_number = self.generate_order_number()
        
        # Calculate total amount
        self.total_amount = (
            self.subtotal - self.discount_amount + 
            self.shipping_cost + self.tax_amount
        )
        
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        import uuid
        from datetime import datetime
        
        # Format: YYYYMMDD-XXXXXX (date + 6 random chars)
        date_str = datetime.now().strftime('%Y%m%d')
        random_str = uuid.uuid4().hex[:6].upper()
        return f'{date_str}-{random_str}'
    
    @property
    def status_display(self):
        """Get status display text"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    @property
    def payment_status_display(self):
        """Get payment status display text"""
        return dict(self.PAYMENT_STATUS_CHOICES).get(self.payment_status, self.payment_status)
    
    @property
    def payment_method_display(self):
        """Get payment method display text"""
        return dict(self.PAYMENT_METHOD_CHOICES).get(self.payment_method, self.payment_method)
    
    @property
    def items_count(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.items.all())
    
    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']
    
    def can_be_returned(self):
        """Check if order can be returned"""
        return self.status == 'delivered'


class OrderItem(models.Model):
    """Order item model"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='الطلب'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='المنتج'
    )
    
    # Product details at time of order (for historical accuracy)
    product_name = models.CharField('اسم المنتج', max_length=200)
    product_price = models.DecimalField(
        'سعر المنتج',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    quantity = models.PositiveIntegerField(
        'الكمية',
        validators=[MinValueValidator(1)]
    )
    
    # Calculated fields
    total_price = models.DecimalField(
        'السعر الإجمالي',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        verbose_name = 'عنصر الطلب'
        verbose_name_plural = 'عناصر الطلبات'
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f'{self.product_name} x {self.quantity}'
    
    def save(self, *args, **kwargs):
        """Override save to calculate total price and store product details"""
        if not self.product_name:
            self.product_name = self.product.name
        if not self.product_price:
            self.product_price = self.product.discounted_price
        
        self.total_price = self.product_price * self.quantity
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Shopping cart model"""
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='المستخدم'
    )
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        verbose_name = 'سلة التسوق'
        verbose_name_plural = 'سلال التسوق'
    
    def __str__(self):
        return f'سلة {self.user.get_full_name()}'
    
    @property
    def items_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_amount(self):
        """Calculate total cart amount"""
        return sum(item.total_price for item in self.items.all())
    
    def clear(self):
        """Clear all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """Cart item model"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='السلة'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='المنتج'
    )
    quantity = models.PositiveIntegerField(
        'الكمية',
        default=1,
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField('تاريخ الإضافة', auto_now_add=True)
    
    class Meta:
        verbose_name = 'عنصر السلة'
        verbose_name_plural = 'عناصر السلة'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    
    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.product.discounted_price * self.quantity
    
    def save(self, *args, **kwargs):
        """Override save to validate stock"""
        if self.quantity > self.product.stock_quantity:
            raise ValueError(f'الكمية المطلوبة ({self.quantity}) أكبر من المتوفر ({self.product.stock_quantity})')
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """Order status change history"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name='الطلب'
    )
    old_status = models.CharField('الحالة السابقة', max_length=20, blank=True)
    new_status = models.CharField('الحالة الجديدة', max_length=20)
    changed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='تم التغيير بواسطة'
    )
    notes = models.TextField('ملاحظات', blank=True)
    changed_at = models.DateTimeField('تاريخ التغيير', auto_now_add=True)
    
    class Meta:
        verbose_name = 'تاريخ حالة الطلب'
        verbose_name_plural = 'تاريخ حالات الطلبات'
        ordering = ['-changed_at']
    
    def __str__(self):
        return f'طلب #{self.order.order_number}: {self.old_status} → {self.new_status}'