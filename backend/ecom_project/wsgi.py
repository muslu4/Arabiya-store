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

# تنفيذ الترحيلات تلقائيًا عند بدء تشغيل التطبيق
try:
    # التحقق مما إذا كان هذا هو أول تشغيل للتطبيق
    if not os.path.exists(BASE_DIR / 'db_initialized.txt'):
        from django.core.management import execute_from_command_line
        from io import StringIO
        
        # تنفيذ الترحيلات
        out = StringIO()
        execute_from_command_line(['manage.py', 'migrate', '--noinput'], stdout=out)
        
        # إنشاء ملف للإشارة إلى أن الترحيلات تم تنفيذها
        with open(BASE_DIR / 'db_initialized.txt', 'w') as f:
            f.write('Database initialized')
except Exception as e:
    # تسجيل الخطأ ولكن لا يوقف تشغيل التطبيق
    print(f"Error during automatic migration: {e}")

application = get_wsgi_application()