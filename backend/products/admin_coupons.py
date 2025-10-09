
from django.contrib import admin
from .models_coupons import Coupon, CouponUsage


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
