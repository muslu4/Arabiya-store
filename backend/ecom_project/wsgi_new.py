"""
WSGI config for ecom_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import sys
import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add the backend directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')

# إنشاء الجداول وتنفيذ الترحيلات تلقائيًا عند بدء تشغيل التطبيق
try:
    # التحقق مما إذا كان هذا هو أول تشغيل للتطبيق
    if not os.path.exists(BASE_DIR / 'db_initialized.txt'):
        from django.core.management import call_command
        from django.db import connection

        # إنشاء الجداول مباشرة
        try:
            # استيراد النماذج
            from users.models import CustomUser
            from products.models import Category, Product
            from orders.models import Order, OrderItem
            from notifications.models import Notification
            from test_app.models import TestModel

            # إنشاء الجداول
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(CustomUser)
                schema_editor.create_model(Category)
                schema_editor.create_model(Product)
                schema_editor.create_model(Order)
                schema_editor.create_model(OrderItem)
                schema_editor.create_model(Notification)
                schema_editor.create_model(TestModel)

            print("Tables created successfully!")
        except Exception as table_error:
            print(f"Error creating tables: {table_error}")
            # محاولة إنشاء الجداول باستخدام الترحيلات
            call_command('makemigrations', 'users', '--noinput')
            call_command('makemigrations', 'products', '--noinput')
            call_command('makemigrations', 'orders', '--noinput')
            call_command('makemigrations', 'notifications', '--noinput')
            call_command('makemigrations', 'test_app', '--noinput')

        # تنفيذ الترحيلات
        call_command('migrate', '--noinput')

        # إنشاء ملف للإشارة إلى أن الترحيلات تم تنفيذها
        with open(BASE_DIR / 'db_initialized.txt', 'w') as f:
            f.write('Database initialized')
except Exception as e:
    # تسجيل الخطأ ولكن لا يوقف تشغيل التطبيق
    print(f"Error during automatic migration: {e}")

application = get_wsgi_application()
