
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)
    fields = ('product', 'name', 'price', 'quantity', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'status', 'total', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_email')
    readonly_fields = ('id', 'created_at', 'updated_at', 'total')
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {
            'fields': ('id', 'customer_name', 'customer_phone', 'customer_email')
        }),
        ('عنوان العميل', {
            'fields': ('customer_address', 'governorate')
        }),
        ('تفاصيل الطلب', {
            'fields': ('status', 'payment_method', 'subtotal', 'delivery_fee', 'total')
        }),
        ('معلومات إضافية', {
            'fields': ('additional_info',)
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # منع إضافة طلبات يدويًا من لوحة الإدارة
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'name', 'price', 'quantity', 'total_price')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('name', 'product__name', 'order__customer_name')
    readonly_fields = ('total_price',)

    fieldsets = (
        (None, {
            'fields': ('order', 'product', 'name', 'price', 'quantity', 'total_price')
        }),
    )

    def has_add_permission(self, request):
        # منع إضافة عناصر طلبات يدويًا من لوحة الإدارة
        return False
