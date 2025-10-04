from django.contrib import admin
from .models import Notification, DeviceToken

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'recipient__username')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('recipient', 'type', 'title', 'message')
        }),
        ('بيانات إضافية', {
            'fields': ('data', 'order'),
            'classes': ('collapse',)
        }),
        ('معلومات النظام', {
            'fields': ('id', 'is_read', 'created_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'device_type', 'is_active', 'created_at')
    list_filter = ('device_type', 'is_active', 'created_at')
    search_fields = ('user__username', 'token')
