from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Order, OrderItem, Cart, CartItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'total_price')
    
    def has_add_permission(self, request, obj=None):
        return False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('old_status', 'new_status', 'changed_by', 'changed_at')
    
    def has_add_permission(self, request, obj=None):
        return False


# Base Order Admin Class
class BaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number_display', 'user_display', 'status_display', 'payment_status_display',
        'total_amount_display', 'items_count_display', 'created_at_display', 'actions_column'
    )
    list_filter = (
        'status', 'payment_status', 'payment_method', 'created_at',
        'shipping_city'
    )
    search_fields = (
        'order_number', 'user__phone', 'user__first_name', 'user__last_name',
        'shipping_name', 'shipping_phone'
    )
    readonly_fields = (
        'order_number', 'created_at', 'updated_at', 'total_amount',
        'items_count', 'user_link', 'order_timeline'
    )
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    list_per_page = 25
    
    fieldsets = (
        ('🛒 معلومات الطلب الأساسية', {
            'fields': ('order_number', 'user', 'user_link', 'created_at', 'updated_at'),
            'classes': ('wide',)
        }),
        ('📊 حالة الطلب والدفع', {
            'fields': ('status', 'payment_status', 'payment_method'),
            'classes': ('wide',)
        }),
        ('💰 تفاصيل التسعير', {
            'fields': ('subtotal', 'discount_amount', 'shipping_cost', 'tax_amount', 'total_amount'),
            'classes': ('wide',)
        }),
        ('🚚 معلومات الشحن والتوصيل', {
            'fields': (
                'shipping_name', 'shipping_phone', 'shipping_address',
                'shipping_city', 'shipping_postal_code'
            ),
            'classes': ('wide',)
        }),
        ('📝 الملاحظات والتعليقات', {
            'fields': ('notes', 'admin_notes'),
            'classes': ('wide', 'collapse')
        }),
        ('⏰ الجدول الزمني للطلب', {
            'fields': ('order_timeline', 'confirmed_at', 'shipped_at', 'delivered_at'),
            'classes': ('wide', 'collapse')
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def order_number_display(self, obj):
        """Display order number with icon"""
        return format_html(
            '<i class="fas fa-receipt" style="color: #6f42c1;"></i> <strong>{}</strong>',
            obj.order_number
        )
    order_number_display.short_description = '🛒 رقم الطلب'
    order_number_display.admin_order_field = 'order_number'
    
    def user_display(self, obj):
        """Display user with link and phone"""
        if obj.user:
            url = reverse('admin:users_user_change', args=[obj.user.id])
            name = obj.user.get_full_name() or 'غير محدد'
            return format_html(
                '<a href="{}" class="badge badge-info"><i class="fas fa-user"></i> {}</a><br><small style="direction: ltr;">📱 {}</small>',
                url, name, obj.user.phone
            )
        return format_html('<span class="badge badge-light">مستخدم محذوف</span>')
    user_display.short_description = '👤 العميل'
    user_display.admin_order_field = 'user__first_name'
    
    def total_amount_display(self, obj):
        """Display total amount with currency"""
        return format_html(
            '<span style="font-weight: bold; color: #28a745; font-size: 1.1em;">{} ر.س</span>',
            obj.total_amount
        )
    total_amount_display.short_description = '💰 المبلغ الإجمالي'
    total_amount_display.admin_order_field = 'total_amount'
    
    def items_count_display(self, obj):
        """Display items count with icon"""
        count = obj.items_count
        return format_html(
            '<span class="badge badge-primary"><i class="fas fa-box"></i> {} عنصر</span>',
            count
        )
    items_count_display.short_description = '📦 عدد العناصر'
    items_count_display.admin_order_field = 'items_count'
    
    def created_at_display(self, obj):
        """Display creation date with icon"""
        return format_html(
            '<i class="fas fa-calendar-plus" style="color: #17a2b8;"></i> {}',
            obj.created_at.strftime('%Y-%m-%d %H:%M')
        )
    created_at_display.short_description = '📅 تاريخ الطلب'
    created_at_display.admin_order_field = 'created_at'
    
    def actions_column(self, obj):
        """Display action buttons"""
        actions = []
        
        # Edit button
        edit_url = reverse('admin:orders_order_change', args=[obj.pk])
        actions.append(f'<a href="{edit_url}" class="btn btn-sm btn-primary" title="تعديل"><i class="fas fa-edit"></i></a>')
        
        # View items button
        items_url = reverse('admin:orders_orderitem_changelist') + f'?order__id__exact={obj.id}'
        actions.append(f'<a href="{items_url}" class="btn btn-sm btn-info" title="عرض العناصر"><i class="fas fa-list"></i></a>')
        
        # Status-specific actions
        if obj.status == 'pending':
            actions.append('<button class="btn btn-sm btn-success" title="تأكيد الطلب"><i class="fas fa-check"></i></button>')
        elif obj.status == 'confirmed':
            actions.append('<button class="btn btn-sm btn-warning" title="شحن الطلب"><i class="fas fa-shipping-fast"></i></button>')
        elif obj.status == 'shipped':
            actions.append('<button class="btn btn-sm btn-info" title="تسليم الطلب"><i class="fas fa-check-double"></i></button>')
        
        # Cancel button (if applicable)
        if obj.status in ['pending', 'confirmed']:
            actions.append('<button class="btn btn-sm btn-danger" title="إلغاء الطلب"><i class="fas fa-times"></i></button>')
        
        return format_html(' '.join(actions))
    actions_column.short_description = '⚡ الإجراءات'
    
    def order_timeline(self, obj):
        """Display order timeline"""
        timeline = []
        
        # Created
        timeline.append(f'<div class="timeline-item"><i class="fas fa-plus-circle text-primary"></i> <strong>تم إنشاء الطلب:</strong> {obj.created_at.strftime("%Y-%m-%d %H:%M")}</div>')
        
        # Confirmed
        if obj.confirmed_at:
            timeline.append(f'<div class="timeline-item"><i class="fas fa-check-circle text-success"></i> <strong>تم التأكيد:</strong> {obj.confirmed_at.strftime("%Y-%m-%d %H:%M")}</div>')
        
        # Shipped
        if obj.shipped_at:
            timeline.append(f'<div class="timeline-item"><i class="fas fa-shipping-fast text-info"></i> <strong>تم الشحن:</strong> {obj.shipped_at.strftime("%Y-%m-%d %H:%M")}</div>')
        
        # Delivered
        if obj.delivered_at:
            timeline.append(f'<div class="timeline-item"><i class="fas fa-check-double text-success"></i> <strong>تم التسليم:</strong> {obj.delivered_at.strftime("%Y-%m-%d %H:%M")}</div>')
        
        return format_html('<div class="order-timeline">{}</div>'.format(''.join(timeline)))
    order_timeline.short_description = 'الجدول الزمني للطلب'
    
    def user_link(self, obj):
        """Display user link for detail view"""
        if obj.user:
            url = reverse('admin:users_user_change', args=[obj.user.id])
            return format_html(
                '<a href="{}" class="btn btn-info btn-sm"><i class="fas fa-user"></i> عرض ملف العميل</a>',
                url
            )
        return format_html('<span class="text-muted">مستخدم محذوف</span>')
    user_link.short_description = 'رابط المستخدم'
    
    def status_display(self, obj):
        """Display order status with colored badge"""
        status_config = {
            'pending': {'color': 'warning', 'icon': 'fas fa-clock', 'text': 'في الانتظار'},
            'confirmed': {'color': 'info', 'icon': 'fas fa-check-circle', 'text': 'مؤكد'},
            'processing': {'color': 'primary', 'icon': 'fas fa-cog', 'text': 'قيد المعالجة'},
            'shipped': {'color': 'secondary', 'icon': 'fas fa-shipping-fast', 'text': 'تم الشحن'},
            'delivered': {'color': 'success', 'icon': 'fas fa-check-double', 'text': 'تم التسليم'},
            'cancelled': {'color': 'danger', 'icon': 'fas fa-times-circle', 'text': 'ملغي'},
            'returned': {'color': 'dark', 'icon': 'fas fa-undo', 'text': 'مرتجع'}
        }
        
        config = status_config.get(obj.status, {'color': 'light', 'icon': 'fas fa-question', 'text': obj.status})
        return format_html(
            '<span class="badge badge-{}"><i class="{}"></i> {}</span>',
            config['color'], config['icon'], config['text']
        )
    status_display.short_description = '📊 حالة الطلب'
    status_display.admin_order_field = 'status'
    
    def payment_status_display(self, obj):
        """Display payment status with colored badge"""
        payment_config = {
            'pending': {'color': 'warning', 'icon': 'fas fa-clock', 'text': 'في الانتظار'},
            'paid': {'color': 'success', 'icon': 'fas fa-check-circle', 'text': 'مدفوع'},
            'failed': {'color': 'danger', 'icon': 'fas fa-times-circle', 'text': 'فشل'},
            'refunded': {'color': 'secondary', 'icon': 'fas fa-undo', 'text': 'مسترد'}
        }
        
        config = payment_config.get(obj.payment_status, {'color': 'light', 'icon': 'fas fa-question', 'text': obj.payment_status})
        return format_html(
            '<span class="badge badge-{}"><i class="{}"></i> {}</span>',
            config['color'], config['icon'], config['text']
        )
    payment_status_display.short_description = '💳 حالة الدفع'
    payment_status_display.admin_order_field = 'payment_status'
    
    def mark_as_confirmed(self, request, queryset):
        updated = 0
        for order in queryset:
            if order.status == 'pending':
                order.status = 'confirmed'
                order.confirmed_at = timezone.now()
                order.save()
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status='pending',
                    new_status='confirmed',
                    changed_by=request.user,
                    notes='تم التأكيد من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'تم تأكيد {updated} طلب')
    mark_as_confirmed.short_description = 'تأكيد الطلبات المحددة'
    
    def mark_as_shipped(self, request, queryset):
        updated = 0
        for order in queryset:
            if order.status in ['confirmed', 'processing']:
                order.status = 'shipped'
                order.shipped_at = timezone.now()
                order.save()
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status=order.status,
                    new_status='shipped',
                    changed_by=request.user,
                    notes='تم الشحن من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'تم شحن {updated} طلب')
    mark_as_shipped.short_description = 'شحن الطلبات المحددة'
    
    def mark_as_delivered(self, request, queryset):
        updated = 0
        for order in queryset:
            if order.status == 'shipped':
                order.status = 'delivered'
                order.delivered_at = timezone.now()
                order.save()
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status='shipped',
                    new_status='delivered',
                    changed_by=request.user,
                    notes='تم التسليم من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'تم تسليم {updated} طلب')
    mark_as_delivered.short_description = 'تسليم الطلبات المحددة'
    
    def mark_as_cancelled(self, request, queryset):
        updated = 0
        for order in queryset:
            if order.can_be_cancelled():
                old_status = order.status
                order.status = 'cancelled'
                order.save()
                
                # Restore stock quantities
                for item in order.items.all():
                    item.product.increase_stock(item.quantity)
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status=old_status,
                    new_status='cancelled',
                    changed_by=request.user,
                    notes='تم الإلغاء من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'🗑️ تم إلغاء {updated} طلب بنجاح')
    mark_as_cancelled.short_description = '🗑️ إلغاء الطلبات المحددة'
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('user').prefetch_related('items__product')
    
    def save_model(self, request, obj, form, change):
        """Custom save with notification"""
        super().save_model(request, obj, form, change)
        if change:
            self.message_user(request, f'✅ تم تحديث الطلب {obj.order_number} بنجاح')
        else:
            self.message_user(request, f'✅ تم إنشاء الطلب {obj.order_number} بنجاح')
    
    class Media:
        css = {
            'all': ('custom_admin.css',)
        }
        js = ('custom_admin.js',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'product_price', 'total_price')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('order__order_number', 'product_name', 'product__name')
    readonly_fields = ('order', 'product', 'product_name', 'product_price', 'total_price')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price', 'added_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'items_count', 'total_amount', 'updated_at')
    search_fields = ('user__phone', 'user__first_name', 'user__last_name')
    readonly_fields = ('user', 'items_count', 'total_amount', 'created_at', 'updated_at')
    inlines = [CartItemInline]
    
    def has_add_permission(self, request):
        return False
    
    def items_count(self, obj):
        return obj.items_count
    items_count.short_description = 'عدد العناصر'
    
    def total_amount(self, obj):
        return f'{obj.total_amount} ر.س'
    total_amount.short_description = 'المبلغ الإجمالي'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('cart__user__phone', 'product__name')
    readonly_fields = ('total_price',)
    
    def total_price(self, obj):
        return f'{obj.total_price} ر.س'
    total_price.short_description = 'السعر الإجمالي'


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('new_status', 'changed_at')
    search_fields = ('order__order_number', 'changed_by__phone')
    readonly_fields = ('order', 'old_status', 'new_status', 'changed_by', 'changed_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# Proxy Models for separating New Orders and Processed Orders
class NewOrder(Order):
    """Proxy model for new/pending orders"""
    class Meta:
        proxy = True
        verbose_name = 'طلب جديد'
        verbose_name_plural = '📥 الطلبات الجديدة'


class ProcessedOrder(Order):
    """Proxy model for processed orders (confirmed, cancelled, etc.)"""
    class Meta:
        proxy = True
        verbose_name = 'طلب'
        verbose_name_plural = '📦 الطلبات'


# Admin for New Orders (Pending only)
class NewOrderAdmin(BaseOrderAdmin):
    """Admin interface for new/pending orders only"""
    
    def get_queryset(self, request):
        """Show only pending orders"""
        qs = super().get_queryset(request)
        return qs.filter(status='pending').select_related('user').prefetch_related('items__product')
    
    actions = ['mark_as_confirmed', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        """Confirm selected orders - they will move to Processed Orders"""
        updated = 0
        for order in queryset:
            if order.status == 'pending':
                order.status = 'confirmed'
                order.confirmed_at = timezone.now()
                order.save()
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status='pending',
                    new_status='confirmed',
                    changed_by=request.user,
                    notes='تم التأكيد من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'✅ تم تأكيد {updated} طلب وتم نقلهم إلى قسم الطلبات')
    mark_as_confirmed.short_description = '✅ تأكيد الطلبات المحددة'
    
    def mark_as_cancelled(self, request, queryset):
        """Cancel selected orders - they will move to Processed Orders"""
        updated = 0
        for order in queryset:
            if order.can_be_cancelled():
                old_status = order.status
                order.status = 'cancelled'
                order.save()
                
                # Restore stock quantities
                for item in order.items.all():
                    if item.product:
                        item.product.increase_stock(item.quantity)
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status=old_status,
                    new_status='cancelled',
                    changed_by=request.user,
                    notes='تم الإلغاء من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'🗑️ تم إلغاء {updated} طلب وتم نقلهم إلى قسم الطلبات')
    mark_as_cancelled.short_description = '🗑️ إلغاء الطلبات المحددة'


# Admin for Processed Orders (All except pending)
class ProcessedOrderAdmin(BaseOrderAdmin):
    """Admin interface for all processed orders (confirmed, shipped, delivered, cancelled)"""
    
    def get_queryset(self, request):
        """Show all orders except pending"""
        qs = super().get_queryset(request)
        return qs.exclude(status='pending').select_related('user').prefetch_related('items__product')
    
    actions = ['mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_shipped(self, request, queryset):
        updated = 0
        for order in queryset:
            if order.status in ['confirmed', 'processing']:
                old_status = order.status
                order.status = 'shipped'
                order.shipped_at = timezone.now()
                order.save()
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status=old_status,
                    new_status='shipped',
                    changed_by=request.user,
                    notes='تم الشحن من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'📦 تم شحن {updated} طلب')
    mark_as_shipped.short_description = '📦 شحن الطلبات المحددة'
    
    def mark_as_delivered(self, request, queryset):
        updated = 0
        for order in queryset:
            if order.status == 'shipped':
                order.status = 'delivered'
                order.delivered_at = timezone.now()
                order.save()
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status='shipped',
                    new_status='delivered',
                    changed_by=request.user,
                    notes='تم التسليم من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'✅ تم تسليم {updated} طلب')
    mark_as_delivered.short_description = '✅ تسليم الطلبات المحددة'
    
    def mark_as_cancelled(self, request, queryset):
        updated = 0
        for order in queryset:
            if order.can_be_cancelled():
                old_status = order.status
                order.status = 'cancelled'
                order.save()
                
                # Restore stock quantities
                for item in order.items.all():
                    if item.product:
                        item.product.increase_stock(item.quantity)
                
                # Create status history
                OrderStatusHistory.objects.create(
                    order=order,
                    old_status=old_status,
                    new_status='cancelled',
                    changed_by=request.user,
                    notes='تم الإلغاء من لوحة الإدارة'
                )
                updated += 1
        
        self.message_user(request, f'🗑️ تم إلغاء {updated} طلب')
    mark_as_cancelled.short_description = '🗑️ إلغاء الطلبات المحددة'


# Register the proxy models
admin.site.register(NewOrder, NewOrderAdmin)
admin.site.register(ProcessedOrder, ProcessedOrderAdmin)

# Keep OrderAdmin as alias for backward compatibility
OrderAdmin = BaseOrderAdmin