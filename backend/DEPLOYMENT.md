# دليل النشر والتشغيل

## متغيرات البيئة المطلوبة

يجب إضافة المتغيرات التالية في لوحة تحكم الاستضافة (مثل Render):

### متغيرات أساسية
- `SECRET_KEY`: مفتاح Django السري
- `DEBUG`: False
- `ALLOWED_HOSTS`: أسماء النطاقات المسموح بها
- `DATABASE_URL`: رابط قاعدة بيانات PostgreSQL

### متغيرات Firebase
- `FIREBASE_CREDENTIALS_JSON`: بيانات اعتماد Firebase بصيغة JSON (انسخ القيمة من ملف firebase_to_env.py)
- `FIREBASE_PROJECT_ID`: ecomproject-a8173

### متغيرات أخرى
- `IMGBB_API_KEY`: مفتاح API لخدمة ImgBB
- `RENDER_FRONTEND_URL`: رابط الواجهة الأمامية

## خطوات النشر

1. رفع المشروع إلى GitHub
2. إضافة متغيرات البيئة في لوحة تحكم الاستضافة
3. ربط قاعدة البيانات PostgreSQL
4. تشغيل النشر

## حل المشاكل الشائعة

### مشكلة اتصال PostgreSQL
تأكد من تثبيت مكتبة `psycopg` وتحديث `requirements.txt`

### مشكلة Firebase
استخدم متغير البيئة `FIREBASE_CREDENTIALS_JSON` بدلاً من رفع الملف مباشرة

### مشكلة الترحيلات
يتم تنفيذ الترحيلات تلقائيًا عند بدء تشغيل التطبيق عبر ملف wsgi.py
