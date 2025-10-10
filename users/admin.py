from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, Notification


# @admin.register(User) - Registered in main admin.py
class UserAdmin(BaseUserAdmin):
    list_display = (
        'phone_display', 'full_name', 'admin_status', 'active_status', 
        'orders_count', 'date_joined_display', 'actions_column'
    )
    list_filter = ('is_admin', 'is_active', 'date_joined', 'last_login')
    search_fields = ('phone', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_per_page = 25
    list_max_show_all = 100
    
    fieldsets = (
        ('🔐 معلومات تسجيل الدخول', {
            'fields': ('phone', 'password'),
            'classes': ('wide',)
        }),
        ('👤 المعلومات الشخصية', {
            'fields': ('first_name', 'last_name', 'device_token'),
            'classes': ('wide',)
        }),
        ('🔑 الصلاحيات والأذونات', {
            'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('wide', 'collapse')
        }),
        ('📅 التواريخ المهمة', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('wide', 'collapse')
        }),
    )
    
    add_fieldsets = (
        ('➕ إضافة مستخدم جديد', {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'first_name', 'last_name', 'is_admin'),
            'description': 'قم بإدخال معلومات المستخدم الجديد'
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    def phone_display(self, obj):
        """Display phone with Saudi flag"""
        if obj.phone:
            return format_html(
                '<span style="direction: ltr;"><i class="fas fa-phone" style="color: #28a745;"></i> 🇸🇦 {}</span>',
                obj.phone
            )
        return '-'
    phone_display.short_description = '📱 رقم الهاتف'
    phone_display.admin_order_field = 'phone'
    
    def full_name(self, obj):
        """Display full name with icon"""
        name = f"{obj.first_name} {obj.last_name}".strip()
        if name:
            return format_html(
                '<i class="fas fa-user" style="color: #6f42c1;"></i> {}',
                name
            )
        return format_html('<span style="color: #6c757d;">غير محدد</span>')
    full_name.short_description = '👤 الاسم الكامل'
    full_name.admin_order_field = 'first_name'
    
    def admin_status(self, obj):
        """Display admin status with badge"""
        if obj.is_admin:
            return format_html(
                '<span class="badge badge-danger"><i class="fas fa-crown"></i> مدير</span>'
            )
        return format_html(
            '<span class="badge badge-secondary"><i class="fas fa-user"></i> مستخدم</span>'
        )
    admin_status.short_description = '👑 نوع الحساب'
    admin_status.admin_order_field = 'is_admin'
    
    def active_status(self, obj):
        """Display active status with colored badge"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success"><i class="fas fa-check-circle"></i> نشط</span>'
            )
        return format_html(
            '<span class="badge badge-warning"><i class="fas fa-pause-circle"></i> معطل</span>'
        )
    active_status.short_description = '✅ حالة الحساب'
    active_status.admin_order_field = 'is_active'
    
    def orders_count(self, obj):
        """Display orders count with link"""
        try:
            count = obj.orders.count() if hasattr(obj, 'orders') else 0
            if count > 0:
                url = reverse('admin:orders_order_changelist') + f'?user__id__exact={obj.id}'
                return format_html(
                    '<a href="{}" class="badge badge-info"><i class="fas fa-shopping-cart"></i> {} طلب</a>',
                    url, count
                )
            return format_html('<span class="badge badge-light">0 طلب</span>')
        except:
            return format_html('<span class="badge badge-light">0 طلب</span>')
    orders_count.short_description = '🛒 عدد الطلبات'
    
    def date_joined_display(self, obj):
        """Display join date with icon"""
        if obj.date_joined:
            return format_html(
                '<i class="fas fa-calendar-plus" style="color: #17a2b8;"></i> {}',
                obj.date_joined.strftime('%Y-%m-%d %H:%M')
            )
        return '-'
    date_joined_display.short_description = '📅 تاريخ التسجيل'
    date_joined_display.admin_order_field = 'date_joined'
    
    def actions_column(self, obj):
        """Display action buttons"""
        actions = []
        
        # Edit button
        edit_url = reverse('admin:users_user_change', args=[obj.pk])
        actions.append(f'<a href="{edit_url}" class="btn btn-sm btn-primary" title="تعديل"><i class="fas fa-edit"></i></a>')
        
        # Delete button
        delete_url = reverse('admin:users_user_delete', args=[obj.pk])
        actions.append(f'<a href="{delete_url}" class="btn btn-sm btn-danger" title="حذف"><i class="fas fa-trash"></i></a>')
        
        # Toggle active status
        if obj.is_active:
            actions.append('<button class="btn btn-sm btn-warning" title="تعطيل الحساب"><i class="fas fa-pause"></i></button>')
        else:
            actions.append('<button class="btn btn-sm btn-success" title="تفعيل الحساب"><i class="fas fa-play"></i></button>')
        
        return format_html(' '.join(actions))
    actions_column.short_description = '⚡ الإجراءات'
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch_related"""
        qs = super().get_queryset(request)
        try:
            qs = qs.prefetch_related('orders')
        except:
            pass
        return qs
    
    def save_model(self, request, obj, form, change):
        """Custom save with notification"""
        super().save_model(request, obj, form, change)
        if change:
            self.message_user(request, f'✅ تم تحديث بيانات المستخدم {obj.phone} بنجاح')
        else:
            self.message_user(request, f'✅ تم إنشاء المستخدم {obj.phone} بنجاح')
    
    def delete_model(self, request, obj):
        """Custom delete with notification"""
        phone = obj.phone
        super().delete_model(request, obj)
        self.message_user(request, f'🗑️ تم حذف المستخدم {phone} بنجاح')
    
    class Media:
        css = {
            'all': ('custom_admin.css',)
        }
        js = ('custom_admin.js',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'level', 'is_read', 'created_at')
    list_filter = ('level', 'is_read', 'created_at')
    search_fields = ('title', 'body', 'recipient__phone', 'recipient__first_name', 'recipient__last_name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'تم تعليم {updated} إشعار كمقروء')
    mark_as_read.short_description = 'تعليم كمقروء'

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'تم تعليم {updated} إشعار كغير مقروء')
    mark_as_unread.short_description = 'تعليم كغير مقروء'