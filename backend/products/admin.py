
from django.contrib import admin
from .models import Category, Product, ProductReview, ProductView, Banner
from .models_coupons import Coupon, CouponUsage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description', 'parent__name')
    prepopulated_fields = {}  # يمكن إضافة حقول يتم ملؤها تلقائيًا إذا لزم الأمر

    fieldsets = (
        (None, {
            'fields': ('name', 'parent', 'description', 'image', 'image_url', 'is_active')
        }),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock_quantity', 'is_active', 'is_featured', 'created_at')
    list_filter = ('category', 'brand', 'is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'brand', 'model')
    list_editable = ('price', 'stock_quantity', 'is_active', 'is_featured')

    fieldsets = (
        ('📦 معلومات أساسية', {
            'fields': ('name', 'description', 'category', 'brand', 'model')
        }),
        ('💰 التسعير والخصومات', {
            'fields': ('price', 'discount_percentage')
        }),
        ('📊 إدارة المخزون', {
            'fields': ('stock_quantity', 'low_stock_threshold')
        }),
        ('🖼️ معرض الصور', {
            'fields': ('main_image', 'image_2', 'image_3', 'image_4')
        }),
        ('🏷️ تفاصيل المنتج', {
            'fields': ('color', 'size', 'weight')
        }),
        ('🔍 SEO والبيانات الوصفية', {
            'fields': ('slug', 'meta_description', 'tags')
        }),
        ('⚡ الحالة والمميزات', {
            'fields': ('is_active', 'is_featured')
        }),
    )


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)


class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('product__name', 'user__username', 'ip_address')
    readonly_fields = ('viewed_at',)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'display_order')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'image_url', 'product', 'link_url')
        }),
        ('إعدادات العرض', {
            'fields': ('is_active', 'display_order')
        }),
    )


# تسجيل نماذج الكوبونات
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """إعدادات عرض الكوبونات في لوحة الإدارة"""
    list_display = [
        'code', 
        'discount_type', 
        'discount_value', 
        'minimum_order_amount',
        'usage_limit',
        'used_count',
        'is_active',
        'start_date',
        'end_date'
    ]
    list_filter = [
        'discount_type',
        'is_active',
        'start_date',
        'end_date',
        'created_at'
    ]
    search_fields = ['code', 'description']
    readonly_fields = ['id', 'used_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('معلومات الكوبون', {
            'fields': (
                'code',
                'description',
                'is_active'
            )
        }),
        ('تفاصيل الخصم', {
            'fields': (
                'discount_type',
                'discount_value',
                'max_discount_amount',
                'minimum_order_amount'
            )
        }),
        ('الصلاحية والاستخدام', {
            'fields': (
                'start_date',
                'end_date',
                'usage_limit',
                'used_count'
            )
        }),
        ('تطبيق الكوبون', {
            'fields': (
                'applicable_products',
                'applicable_categories',
                'excluded_products',
                'excluded_categories'
            )
        }),
        ('معلومات النظام', {
            'fields': (
                'id',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        """جعل حقل used_count للقراءة فقط دائمًا"""
        if obj:  # إذا كان الكائن موجودًا بالفعل
            return self.readonly_fields + ['used_count']
        return self.readonly_fields


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    """إعدادات عرض استخدامات الكوبونات في لوحة الإدارة"""
    list_display = [
        'coupon_code',
        'user',
        'order',
        'discount_amount',
        'used_at'
    ]
    list_filter = [
        'used_at',
        'coupon__discount_type'
    ]
    search_fields = [
        'coupon__code',
        'user__first_name',
        'user__last_name',
        'user__phone',
        'order__id'
    ]
    readonly_fields = ['id', 'used_at']
    
    def coupon_code(self, obj):
        """عرض كود الكوبون"""
        return obj.coupon.code
    coupon_code.short_description = 'كود الكوبون'
    
    def has_add_permission(self, request):
        """منع إضافة استخدامات كوبونات يدويًا"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """منع تعديل استخدامات الكوبونات"""
        return False
