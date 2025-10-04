
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = 'الإشعارات'

    def ready(self):
        """
        Initialize Firebase when the app is ready.
        """
        from . import firebase_service
        firebase_service.initialize_firebase()
