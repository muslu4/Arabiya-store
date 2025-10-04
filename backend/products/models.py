from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Category(models.Model):
    """Product category model"""
    name = models.CharField('اسم القسم', max_length=100, unique=True)
    description = models.TextField('الوصف', blank=True)
    image = models.ImageField('صورة القسم', upload_to='categories/', blank=True, null=True)
    image_url = models.URLField('رابط صورة القسم (الخارجي)', blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children', verbose_name='القسم الأب'
    )
    is_active = models.BooleanField('نشط', default=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        verbose_name = 'قسم'
        verbose_name_plural = 'الأقسام'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def products_count(self):
        """Get number of active products in this category (direct products only)"""
        return self.products.filter(is_active=True).count()

    @property
    def children_count(self):
        """Get number of active direct subcategories"""
        return self.children.filter(is_active=True).count()


class Product(models.Model):
    """Product model"""
    name = models.CharField('اسم المنتج', max_length=200)
    description = models.TextField('الوصف')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='القسم'
    )
    
    # Pricing
    price = models.DecimalField(
        'السعر',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    discount_percentage = models.IntegerField(
        'نسبة الخصم',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Inventory
    stock_quantity = models.PositiveIntegerField('الكمية المتوفرة', default=0)
    low_stock_threshold = models.PositiveIntegerField('حد التنبيه للمخزون', default=10)
    
    # Images (store direct URLs from ImgBB)
    main_image = models.URLField('رابط الصورة الرئيسية (ImgBB)', blank=True, null=True)
    image_2 = models.URLField('رابط الصورة الثانية (ImgBB)', blank=True, null=True)
    image_3 = models.URLField('رابط الصورة الثالثة (ImgBB)', blank=True, null=True)
    image_4 = models.URLField('رابط الصورة الرابعة (ImgBB)', blank=True, null=True)
    
    # Product details
    brand = models.CharField('العلامة التجارية', max_length=100, blank=True)
    model = models.CharField('الموديل', max_length=100, blank=True)
    color = models.CharField('اللون', max_length=50, blank=True)
    size = models.CharField('المقاس', max_length=50, blank=True)
    weight = models.DecimalField(
        'الوزن (كجم)',
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    
    # SEO and metadata
    slug = models.SlugField('الرابط', max_length=250, unique=True, blank=True)
    meta_description = models.CharField('وصف SEO', max_length=160, blank=True)
    tags = models.CharField('الكلمات المفتاحية', max_length=500, blank=True)
    
    # Status
    is_active = models.BooleanField('نشط', default=True)
    is_featured = models.BooleanField('منتج مميز', default=False)
    
    # Timestamps
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Override save to generate slug"""
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    @property
    def discounted_price(self):
        """Calculate discounted price"""
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price
    
    @property
    def is_on_sale(self):
        """Check if product is on sale"""
        return self.discount_percentage > 0
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self):
        """Check if product is low in stock"""
        return 0 < self.stock_quantity <= self.low_stock_threshold
    
    @property
    def stock_status(self):
        """Get stock status"""
        if self.stock_quantity == 0:
            return 'out_of_stock'
        elif self.is_low_stock:
            return 'low_stock'
        else:
            return 'in_stock'
    
    @property
    def stock_status_display(self):
        """Get stock status display text"""
        status_map = {
            'out_of_stock': 'نفد المخزون',
            'low_stock': 'مخزون منخفض',
            'in_stock': 'متوفر'
        }
        return status_map.get(self.stock_status, 'غير محدد')
    
    @property
    def all_images(self):
        """Get all product image URLs (strings)"""
        images = []
        for img in [self.main_image, self.image_2, self.image_3, self.image_4]:
            if img:
                images.append(img)
        return images
    
    def reduce_stock(self, quantity):
        """Reduce stock quantity"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save(update_fields=['stock_quantity'])
            return True
        return False
    
    def increase_stock(self, quantity):
        """Increase stock quantity"""
        self.stock_quantity += quantity
        self.save(update_fields=['stock_quantity'])


class ProductReview(models.Model):
    """Product review model"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='المنتج'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='المستخدم'
    )
    rating = models.IntegerField(
        'التقييم',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField('التعليق', blank=True)
    is_approved = models.BooleanField('معتمد', default=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    
    class Meta:
        verbose_name = 'تقييم المنتج'
        verbose_name_plural = 'تقييمات المنتجات'
        unique_together = ['product', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.get_full_name()} - {self.product.name} ({self.rating}/5)'


class ProductView(models.Model):
    """Product view tracking"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name='المنتج'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='المستخدم'
    )
    ip_address = models.GenericIPAddressField('عنوان IP', blank=True, null=True)
    user_agent = models.TextField('معلومات المتصفح', blank=True)
    viewed_at = models.DateTimeField('تاريخ المشاهدة', default=timezone.now)
    
    class Meta:
        verbose_name = 'مشاهدة المنتج'
        verbose_name_plural = 'مشاهدات المنتجات'
        ordering = ['-viewed_at']
    
    def __str__(self):
        user_info = self.user.get_full_name() if self.user else self.ip_address
        return f'{user_info} - {self.product.name}'


class Banner(models.Model):
    """Banner/Advertisement model for homepage slider"""
    title = models.CharField('عنوان الإعلان', max_length=200)
    description = models.TextField('وصف الإعلان', blank=True)
    image = models.ImageField('صورة الإعلان', upload_to='banners/')
    image_url = models.URLField('رابط صورة الإعلان (الخارجي)', blank=True, null=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='banners',
        verbose_name='المنتج المرتبط',
        null=True,
        blank=True
    )
    link_url = models.URLField('رابط التوجيه', blank=True, null=True)
    is_active = models.BooleanField('نشط', default=True)
    display_order = models.PositiveIntegerField('ترتيب العرض', default=0)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = 'إعلان'
        verbose_name_plural = 'الإعلانات'
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    def get_link(self):
        """Get the link URL for the banner"""
        if self.product:
            return f"/product/{self.product.slug}/"
        return self.link_url or "#"

    def get_image_url(self):
        """Get the image URL for the banner"""
        if self.image:
            return self.image.url
        return self.image_url or "#"