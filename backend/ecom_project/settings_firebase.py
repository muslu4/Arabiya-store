"""
إعدادات Firebase للتطبيق باستخدام متغير البيئة
"""

import os
import json

# معرف مشروع Firebase (يمكن تركه ثابتًا)
FIREBASE_PROJECT_ID = 'ecomproject-a8173'

# تهيئة Firebase
try:
    import firebase_admin
    from firebase_admin import credentials

    # قراءة بيانات الاعتماد من متغير البيئة
    firebase_credentials_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
    if not firebase_credentials_json:
        raise ValueError("متغير البيئة FIREBASE_CREDENTIALS_JSON غير معرف")

    cred_dict = json.loads(firebase_credentials_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

    print("تم تهيئة Firebase بنجاح")
except ImportError:
    print("لم يتم تثبيت مكتبة Firebase Admin")
except Exception as e:
    print(f"حدث خطأ أثناء تهيئة Firebase: {e}")
