
from django.contrib import admin
from .models import Category, Product, ProductReview, ProductView, Banner


@admin.register(Category)
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


@admin.register(Product)
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


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('product__name', 'user__username', 'ip_address')
    readonly_fields = ('viewed_at',)


@admin.register(Banner)
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
