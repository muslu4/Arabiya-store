from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Order
from users.models import User
from notifications.models import Notification

# Firebase service for push notifications
try:
    from backend.firebase_service import initialize_firebase, send_notification_to_device
except Exception:
    initialize_firebase = None
    send_notification_to_device = None


@receiver(post_save, sender=Order)
def notify_admins_on_new_order(sender, instance: Order, created: bool, **kwargs):
    """
    When a new order is created, create a Notification in DB and push FCM to admins.
    """
    try:
        if not created:
            return

        order = instance
        title = f"طلب جديد #{order.order_number}"
        body = (
            f"المستخدم: {order.user.get_full_name()} — العدد: {order.items_count} — المبلغ: {order.total_amount}"
        )

        # Create a single DB notification (global, no specific recipient)
        Notification.objects.create(
            title=title,
            body=body,
            recipient=None,
            level='info',
            created_at=timezone.now(),
        )

        # Send FCM push to all admin users who have a device token
        if initialize_firebase and send_notification_to_device:
            try:
                initialize_firebase()
            except Exception:
                pass

            admin_tokens = list(
                User.objects.filter(is_admin=True).exclude(device_token__isnull=True).exclude(device_token__exact='')
                .values_list('device_token', flat=True)
            )
            for token in admin_tokens:
                try:
                    send_notification_to_device(
                        token=token,
                        title=title,
                        body=body,
                        data={
                            'type': 'new_order',
                            'order_number': order.order_number,
                            'order_id': str(order.id),
                        }
                    )
                except Exception:
                    # Avoid breaking the signal on FCM failure
                    continue
    except Exception:
        # Never crash on signal
        return