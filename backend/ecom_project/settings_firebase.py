
"""
إعدادات Firebase للتطبيق
"""

import os
from django.conf import settings

# مسار ملف بيانات اعتماد Firebase
FIREBASE_CREDENTIALS_PATH = os.path.join(settings.BASE_DIR, 'firebase', 'ecomproject-a8173-38763797948f.json')

# معرف مشروع Firebase
FIREBASE_PROJECT_ID = 'ecomproject-a8173'

# تهيئة Firebase
try:
    import firebase_admin
    from firebase_admin import credentials
    from .firebase_utils import initialize_firebase

    # تهيئة Firebase عند بدء تشغيل التطبيق
    initialize_firebase()
except ImportError:
    print("لم يتم تثبيت مكتبة Firebase Admin")
except Exception as e:
    print(f"حدث خطأ أثناء تهيئة Firebase: {e}")
