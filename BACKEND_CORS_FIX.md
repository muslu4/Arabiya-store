# إصلاح إعدادات CORS في الباكند

## المشكلة
الواجهة الأمامية لا يمكنها الاتصال بالباكند بسبب إعدادات CORS غير الصحيحة.

## الحل
تم تحديث ملف settings.py في الباكند:

### 1. تحديث RENDER_FRONTEND_URL
- تم تغيير القيمة الافتراضية من '' إلى 'https://ecom-parent-project-1.onrender.com'

### 2. تحديث إعدادات CORS في بيئة الإنتاج
- تم تعديل إعدادات CORS للسماح بالوصول من الواجهة الأمامية على Render
- تم إضافة عنوان الواجهة الأمامية إلى قائمة المصادر المسموح بها في بيئة الإنتاج

## التغييرات المحددة
```python
# Render frontend URL
RENDER_FRONTEND_URL = config('RENDER_FRONTEND_URL', default='https://ecom-parent-project-1.onrender.com')
if RENDER_FRONTEND_URL:
    CORS_ALLOWED_ORIGINS.append(RENDER_FRONTEND_URL)

# Allow file:// protocol for local HTML files
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True  # For development only
else:
    # In production, only allow specific origins
    CORS_ALLOWED_ORIGINS.append('https://ecom-parent-project-1.onrender.com')
CORS_ALLOW_CREDENTIALS = True
```

## الخطوات التالية
1. قم بإعادة نشر الباكند على Render لتطبيق إعدادات CORS الجديدة
2. تحقق من أن الواجهة الأمامية يمكنها الآن الاتصال بالباكند

## النتائج المتوقعة
بعد تطبيق هذه التغييرات، يجب أن تتمكن الواجهة الأمامية من الاتصال بالباكند وجلب البيانات بشكل صحيح.
