from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = 'الطلبات'

    def ready(self):
        # Import signals to connect receivers
        from . import signals  # noqa: F401