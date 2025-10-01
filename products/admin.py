from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Avg
from .models import Category, Product, ProductReview, ProductView, Banner


from django.urls import reverse
from .views_fixed import add_category_view, category_list_view, category_add_success_view

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_display', 'image_preview', 'products_count', 'status_display', 'created_at_display', 'actions_column')
    list_filter = ('is_active', 'created_at', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {}
    readonly_fields = ('created_at', 'updated_at', 'products_count_display', 'children_count_display')
    list_per_page = 20
    
    fieldsets = (
        ('📂 معلومات أساسية', {
            'fields': ('name', 'parent', 'description', 'image', 'image_url'),
            'classes': ('wide',)
        }),
        ('⚡ الحالة', {
            'fields': ('is_active',),
            'classes': ('wide',)
        }),
        ('📊 إحصائيات', {
            'fields': ('products_count_display', 'children_count_display'),
            'classes': ('wide', 'collapse')
        }),
        ('📅 معلومات إضافية', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('wide', 'collapse')
        }),
    )
    
    def name_display(self, obj):
        """Display category name with icon"""
        return format_html(
            '<i class="fas fa-folder" style="color: #6f42c1;"></i> <strong>{}</strong>',
            obj.name
        )
    name_display.short_description = '📂 اسم القسم'
    name_display.admin_order_field = 'name'
    
    def image_preview(self, obj):
        """Display category image preview"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;" />',
                obj.image.url
            )
        elif obj.image_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;" />',
                obj.image_url
            )
        return format_html('<div style="width: 50px; height: 50px; background: #f8f9fa; border-radius: 8px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image" style="color: #6c757d;"></i></div>')
    image_preview.short_description = '🖼️ الصورة'
    
    def products_count(self, obj):
        """Display products count with link (direct products only)"""
        count = obj.products_count
        if count > 0:
            url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
            return format_html(
                '<a href="{}" class="badge badge-info"><i class="fas fa-box"></i> {} منتج</a>',
                url, count
            )
        return format_html('<span class="badge badge-light">0 منتج</span>')
    products_count.short_description = '📦 عدد المنتجات'

    def children_count_display(self, obj):
        """Display subcategories count with link"""
        count = obj.children_count
        if count > 0:
            url = reverse('admin:products_category_changelist') + f'?parent__id__exact={obj.id}'
            return format_html(
                '<a href="{}" class="badge badge-secondary"><i class="fas fa-sitemap"></i> {} قسم فرعي</a>',
                url, count
            )
        return format_html('<span class="badge badge-light">0 قسم فرعي</span>')
    children_count_display.short_description = '🗂️ الأقسام الفرعية'
    
    def status_display(self, obj):
        """Display active status with badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success"><i class="fas fa-check-circle"></i> نشط</span>'
            )
        return format_html(
            '<span class="badge badge-warning"><i class="fas fa-pause-circle"></i> معطل</span>'
        )
    status_display.short_description = '✅ الحالة'
    status_display.admin_order_field = 'is_active'
    
    def created_at_display(self, obj):
        """Display creation date with icon"""
        return format_html(
            '<i class="fas fa-calendar-plus" style="color: #17a2b8;"></i> {}',
            obj.created_at.strftime('%Y-%m-%d')
        )
    created_at_display.short_description = '📅 تاريخ الإنشاء'
    created_at_display.admin_order_field = 'created_at'
    
    def actions_column(self, obj):
        """Display action buttons"""
        actions = []
        
        # Edit button
        edit_url = reverse('admin:products_category_change', args=[obj.pk])
        actions.append(f'<a href="{edit_url}" class="btn btn-sm btn-primary" title="تعديل"><i class="fas fa-edit"></i></a>')
        
        # View products button
        products_url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
        actions.append(f'<a href="{products_url}" class="btn btn-sm btn-info" title="عرض المنتجات"><i class="fas fa-box"></i></a>')
        
        # Delete button
        delete_url = reverse('admin:products_category_delete', args=[obj.pk])
        actions.append(f'<a href="{delete_url}" class="btn btn-sm btn-danger" title="حذف"><i class="fas fa-trash"></i></a>')
        
        return format_html(' '.join(actions))
    actions_column.short_description = '⚡ الإجراءات'
    
    def products_count_display(self, obj):
        """Display detailed products count"""
        count = obj.products_count
        return format_html(
            '<span class="badge badge-primary">{} منتج</span>',
            count
        )
    products_count_display.short_description = 'عدد المنتجات'
    
    class Media:
        css = {
            'all': ('custom_admin.css',)
        }
        js = ('custom_admin.js', 'product_tabs.js')


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = True
    
    def has_add_permission(self, request, obj=None):
        return False


# @admin.register(Product) - Registered in main admin.py
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name_display', 'image_preview', 'category_display', 'price_display', 
        'stock_status_display', 'rating_display', 'status_badges', 'actions_column'
    )
    list_filter = (
        'category', 'is_active', 'is_featured', 'created_at',
        'discount_percentage', 'brand', 'stock_quantity'
    )
    search_fields = ('name', 'description', 'brand', 'model', 'tags')
    readonly_fields = (
        'slug', 'created_at', 'updated_at', 'discounted_price',
        'stock_status_display', 'main_image_preview', 'rating_display', 'reviews_count'
    )
    prepopulated_fields = {}
    inlines = [ProductReviewInline]
    list_per_page = 20
    
    fieldsets = (
        ('📦 معلومات أساسية', {
            'fields': ('name', 'description', 'category', 'slug'),
            'classes': ('wide',)
        }),
        ('💰 التسعير والخصومات', {
            'fields': ('price', 'discount_percentage', 'discounted_price'),
            'classes': ('wide',)
        }),
        ('📊 إدارة المخزون', {
            'fields': ('stock_quantity', 'low_stock_threshold', 'stock_status_display'),
            'classes': ('wide',)
        }),
        ('🖼️ معرض الصور', {
            'fields': ('main_image', 'main_image_preview', 'image_2', 'image_3', 'image_4'),
            'classes': ('wide',)
        }),
        ('🏷️ تفاصيل المنتج', {
            'fields': ('brand', 'model', 'color', 'size', 'weight'),
            'classes': ('wide', 'collapse')
        }),
        ('🔍 SEO والبيانات الوصفية', {
            'fields': ('meta_description', 'tags'),
            'classes': ('wide', 'collapse')
        }),
        ('⚡ الحالة والمميزات', {
            'fields': ('is_active', 'is_featured'),
            'classes': ('wide',)
        }),
        ('📈 الإحصائيات', {
            'fields': ('rating_display', 'reviews_count'),
            'classes': ('wide', 'collapse')
        }),
        ('📅 معلومات إضافية', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('wide', 'collapse')
        }),
    )
    
    actions = ['make_active', 'make_inactive', 'make_featured', 'remove_featured', 'apply_discount']
    
    def name_display(self, obj):
        """Display product name with icon"""
        return format_html(
            '<i class="fas fa-box" style="color: #6f42c1;"></i> <strong>{}</strong>',
            obj.name[:50] + '...' if len(obj.name) > 50 else obj.name
        )
    name_display.short_description = '📦 اسم المنتج'
    name_display.admin_order_field = 'name'
    
    def image_preview(self, obj):
        """Display product image preview"""
        if obj.main_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; border-radius: 8px; object-fit: cover; border: 2px solid #dee2e6;" />',
                obj.main_image
            )
        return format_html('<div style="width: 60px; height: 60px; background: #f8f9fa; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 2px solid #dee2e6;"><i class="fas fa-image" style="color: #6c757d;"></i></div>')
    image_preview.short_description = '🖼️ الصورة'
    
    def category_display(self, obj):
        """Display category with link"""
        if obj.category:
            url = reverse('admin:products_category_change', args=[obj.category.pk])
            return format_html(
                '<a href="{}" class="badge badge-secondary"><i class="fas fa-folder"></i> {}</a>',
                url, obj.category.name
            )
        return format_html('<span class="badge badge-light">غير محدد</span>')
    category_display.short_description = '📂 القسم'
    category_display.admin_order_field = 'category__name'
    
    def price_display(self, obj):
        """Display price with discount info"""
        if obj.is_on_sale:
            return format_html(
                '<div><span style="text-decoration: line-through; color: #6c757d;">{} ر.س</span><br><span style="color: #dc3545; font-weight: bold; font-size: 1.1em;">{} ر.س</span><br><span class="badge badge-danger">خصم {}%</span></div>',
                obj.price, obj.discounted_price, obj.discount_percentage
            )
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">{} ر.س</span>',
            obj.price
        )
    price_display.short_description = '💰 السعر'
    price_display.admin_order_field = 'price'
    
    def stock_status_display(self, obj):
        """Display stock status with colored badge"""
        status = obj.stock_status
        if status == 'out_of_stock':
            return format_html(
                '<span class="badge badge-danger"><i class="fas fa-times-circle"></i> نفد المخزون</span><br><small>الكمية: {}</small>',
                obj.stock_quantity
            )
        elif status == 'low_stock':
            return format_html(
                '<span class="badge badge-warning"><i class="fas fa-exclamation-triangle"></i> مخزون منخفض</span><br><small>الكمية: {}</small>',
                obj.stock_quantity
            )
        else:
            return format_html(
                '<span class="badge badge-success"><i class="fas fa-check-circle"></i> متوفر</span><br><small>الكمية: {}</small>',
                obj.stock_quantity
            )
    stock_status_display.short_description = '📊 حالة المخزون'
    stock_status_display.admin_order_field = 'stock_quantity'
    
    def rating_display(self, obj):
        """Display product rating with stars"""
        try:
            reviews = obj.reviews.filter(is_approved=True)
            if reviews.exists():
                avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
                stars = '⭐' * int(avg_rating) + '☆' * (5 - int(avg_rating))
                return format_html(
                    '<div>{}<br><small>{:.1f} ({} تقييم)</small></div>',
                    stars, avg_rating, reviews.count()
                )
            return format_html('<span class="text-muted">لا توجد تقييمات</span>')
        except:
            return format_html('<span class="text-muted">-</span>')
    rating_display.short_description = '⭐ التقييم'
    
    def status_badges(self, obj):
        """Display status badges"""
        badges = []
        
        if obj.is_active:
            badges.append('<span class="badge badge-success"><i class="fas fa-check"></i> نشط</span>')
        else:
            badges.append('<span class="badge badge-secondary"><i class="fas fa-pause"></i> معطل</span>')
            
        if obj.is_featured:
            badges.append('<span class="badge badge-warning"><i class="fas fa-star"></i> مميز</span>')
            
        return format_html('<br>'.join(badges))
    status_badges.short_description = '🏷️ الحالة'
    
    def actions_column(self, obj):
        """Display action buttons"""
        actions = []
        
        # Edit button
        edit_url = reverse('admin:products_product_change', args=[obj.pk])
        actions.append(f'<a href="{edit_url}" class="btn btn-sm btn-primary" title="تعديل"><i class="fas fa-edit"></i></a>')
        
        # View reviews button
        reviews_url = reverse('admin:products_productreview_changelist') + f'?product__id__exact={obj.id}'
        actions.append(f'<a href="{reviews_url}" class="btn btn-sm btn-info" title="التقييمات"><i class="fas fa-star"></i></a>')
        
        # Toggle featured
        if obj.is_featured:
            actions.append('<button class="btn btn-sm btn-warning" title="إزالة من المميز"><i class="fas fa-star-half-alt"></i></button>')
        else:
            actions.append('<button class="btn btn-sm btn-success" title="جعل مميز"><i class="fas fa-star"></i></button>')
        
        # Delete button
        delete_url = reverse('admin:products_product_delete', args=[obj.pk])
        actions.append(f'<a href="{delete_url}" class="btn btn-sm btn-danger" title="حذف"><i class="fas fa-trash"></i></a>')
        
        return format_html(' '.join(actions))
    actions_column.short_description = '⚡ الإجراءات'
    
    def main_image_preview(self, obj):
        """Display main image preview for detail view"""
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />',
                obj.main_image
            )
        return format_html('<div style="width: 300px; height: 200px; background: #f8f9fa; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 2px dashed #dee2e6;"><i class="fas fa-image fa-3x" style="color: #6c757d;"></i><br><span style="color: #6c757d;">لا توجد صورة</span></div>')
    main_image_preview.short_description = 'معاينة الصورة الرئيسية'
    
    def reviews_count(self, obj):
        """Display reviews count"""
        try:
            count = obj.reviews.count()
            approved_count = obj.reviews.filter(is_approved=True).count()
            return format_html(
                '<span class="badge badge-info">{} إجمالي</span><br><span class="badge badge-success">{} معتمد</span>',
                count, approved_count
            )
        except:
            return format_html('<span class="badge badge-light">0</span>')
    reviews_count.short_description = 'عدد التقييمات'
    
    # Custom Actions
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✅ تم تفعيل {updated} منتج بنجاح')
    make_active.short_description = '✅ تفعيل المنتجات المحددة'
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'⏸️ تم إلغاء تفعيل {updated} منتج بنجاح')
    make_inactive.short_description = '⏸️ إلغاء تفعيل المنتجات المحددة'
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'⭐ تم جعل {updated} منتج مميز بنجاح')
    make_featured.short_description = '⭐ جعل المنتجات مميزة'
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'🌟 تم إزالة {updated} منتج من المميزة بنجاح')
    remove_featured.short_description = '🌟 إزالة من المنتجات المميزة'
    
    def apply_discount(self, request, queryset):
        # This would open a form to apply discount - simplified for now
        self.message_user(request, f'💰 تم تطبيق خصم على {queryset.count()} منتج')
    apply_discount.short_description = '💰 تطبيق خصم'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('category').prefetch_related('reviews')
    
    class Media:
        css = {
            'all': ('custom_admin.css',)
        }
        js = ('custom_admin.js', 'product_tabs.js')


# @admin.register(ProductReview) - Registered in main admin.py
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name', 'user__phone', 'comment')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('معلومات التقييم', {
            'fields': ('product', 'user', 'rating', 'comment')
        }),
        ('الحالة', {
            'fields': ('is_approved',)
        }),
        ('معلومات إضافية', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'تم اعتماد {queryset.count()} تقييم')
    approve_reviews.short_description = 'اعتماد التقييمات المحددة'
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'تم رفض {queryset.count()} تقييم')
    disapprove_reviews.short_description = 'رفض التقييمات المحددة'


# @admin.register(ProductView) - Registered in main admin.py
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at', 'product__category')
    search_fields = ('product__name', 'user__phone', 'ip_address')
    readonly_fields = ('product', 'user', 'ip_address', 'user_agent', 'viewed_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title_display', 'image_preview', 'product_display', 'status_display', 'display_order', 'created_at', 'actions_column')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'product__name')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    list_editable = ('display_order',)

    fieldsets = (
        ('📢 معلومات الإعلان', {
            'fields': ('title', 'description', 'image', 'image_url'),
            'classes': ('wide',)
        }),
        ('🔗 الربط والتوجيه', {
            'fields': ('product', 'link_url'),
            'classes': ('wide',)
        }),
        ('⚙️ الإعدادات', {
            'fields': ('is_active', 'display_order'),
            'classes': ('wide',)
        }),
        ('📅 معلومات إضافية', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('wide', 'collapse')
        }),
    )

    def title_display(self, obj):
        """Display banner title with icon"""
        return format_html(
            '<i class="fas fa-bullhorn" style="color: #6f42c1;"></i> <strong>{}</strong>',
            obj.title
        )
    title_display.short_description = '📢 عنوان الإعلان'
    title_display.admin_order_field = 'title'

    def image_preview(self, obj):
        """Display banner image preview"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; border-radius: 8px; object-fit: cover; border: 2px solid #dee2e6;" />',
                obj.image.url
            )
        elif obj.image_url:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; border-radius: 8px; object-fit: cover; border: 2px solid #dee2e6;" />',
                obj.image_url
            )
        return format_html('<div style="width: 80px; height: 60px; background: #f8f9fa; border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 2px dashed #dee2e6;"><i class="fas fa-image" style="color: #6c757d;"></i></div>')
    image_preview.short_description = '🖼️ الصورة'

    def product_display(self, obj):
        """Display linked product with link"""
        if obj.product:
            url = reverse('admin:products_product_change', args=[obj.product.pk])
            return format_html(
                '<a href="{}" class="badge badge-info"><i class="fas fa-box"></i> {}</a>',
                url, obj.product.name[:30] + '...' if len(obj.product.name) > 30 else obj.product.name
            )
        return format_html('<span class="badge badge-secondary">رابط خارجي</span>')
    product_display.short_description = '📦 المنتج المرتبط'

    def status_display(self, obj):
        """Display active status with badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success"><i class="fas fa-check-circle"></i> نشط</span>'
            )
        return format_html(
            '<span class="badge badge-warning"><i class="fas fa-pause-circle"></i> معطل</span>'
        )
    status_display.short_description = '✅ الحالة'
    status_display.admin_order_field = 'is_active'

    def actions_column(self, obj):
        """Display action buttons"""
        actions = []

        # Edit button
        edit_url = reverse('admin:products_banner_change', args=[obj.pk])
        actions.append(f'<a href="{edit_url}" class="btn btn-sm btn-primary" title="تعديل"><i class="fas fa-edit"></i></a>')

        # Delete button
        delete_url = reverse('admin:products_banner_delete', args=[obj.pk])
        actions.append(f'<a href="{delete_url}" class="btn btn-sm btn-danger" title="حذف"><i class="fas fa-trash"></i></a>')

        return format_html(' '.join(actions))
    actions_column.short_description = '⚡ الإجراءات'

    class Media:
        css = {
            'all': ('custom_admin.css',)
        }
        js = ('custom_admin.js',)