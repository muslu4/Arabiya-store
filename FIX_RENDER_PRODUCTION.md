# 🔧 إصلاح مشكلة الإنتاج على Render

## ❌ المشكلة
```
django.db.utils.ProgrammingError: relation "django_session" does not exist
```

**السبب**: قاعدة بيانات PostgreSQL على Render لا تحتوي على الجداول المطلوبة.

---

## ✅ الحل: تشغيل Migrations على Render

### الطريقة 1: من لوحة تحكم Render (الأسهل)

1. **افتح Dashboard على Render**
   - اذهب إلى: https://dashboard.render.com/
   - اختر مشروعك: `ecom-parent-project`

2. **افتح Shell**
   - اضغط على تبويب **"Shell"** في الأعلى
   - أو اذهب لـ **"Manual Deploy"** > **"Shell"**

3. **شغّل الأوامر التالية**:
   ```bash
   cd backend
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **أدخل بيانات المدير**:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `admin123`

---

### الطريقة 2: إعادة النشر (Redeploy)

1. **افتح Dashboard على Render**
2. **اذهب لمشروعك**
3. **اضغط "Manual Deploy"**
4. **اختر "Clear build cache & deploy"**

هذا سيشغل ملف `build.sh` الذي يحتوي على:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

### الطريقة 3: التحقق من ملف build.sh

تأكد أن ملف `backend/build.sh` يحتوي على:

```bash
#!/bin/bash

# تثبيت المتطلبات
pip install -r requirements.txt

# ترحيل قاعدة البيانات
python manage.py makemigrations
python manage.py migrate

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# إنشاء مستخدم مدير
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
```

---

## 🔍 التحقق من نجاح الإصلاح

بعد تشغيل الأوامر، جرب:

1. **افتح صفحة الإدارة**:
   ```
   https://ecom-parent-project.onrender.com/admin/
   ```

2. **سجل الدخول**:
   - Username: `admin`
   - Password: `admin123`

3. **تحقق من الكوبونات**:
   ```
   https://ecom-parent-project.onrender.com/admin/products/coupon/
   ```

---

## 📝 ملاحظات مهمة

### ✅ التحديثات المطبقة محلياً:

1. **تسجيل الكوبونات في Admin Site المخصص**
   - ملف: `backend/ecom_project/admin.py`
   - تم إضافة: `Coupon` و `CouponUsage`

2. **إزالة التسجيل المزدوج**
   - ملف: `backend/products/admin.py`
   - تم إزالة: `@admin.register()` decorators

### 🚀 لرفع التحديثات للمستودع:

```bash
# في مجلد المستودع
git add .
git commit -m "Fix: Register Coupons in custom admin site"
git push origin main
```

أو استخدم الملف:
```
PUSH_TO_GIT.bat
```

---

## 🆘 إذا استمرت المشكلة

### تحقق من متغيرات البيئة على Render:

1. **DATABASE_URL**: يجب أن يكون موجود ويشير لـ PostgreSQL
2. **DEBUG**: يجب أن يكون `False`
3. **SECRET_KEY**: يجب أن يكون موجود
4. **ALLOWED_HOSTS**: يجب أن يحتوي على `ecom-parent-project.onrender.com`

### تحقق من Logs:

1. اذهب لـ Render Dashboard
2. اختر مشروعك
3. اضغط على **"Logs"**
4. ابحث عن أخطاء في:
   - Build logs
   - Deploy logs
   - Runtime logs

---

## 📞 الدعم

إذا واجهت أي مشكلة:

1. **تحقق من Logs على Render**
2. **تأكد من تشغيل migrations**
3. **تحقق من اتصال قاعدة البيانات**
4. **جرب Clear Cache & Redeploy**

---

## ✅ الخلاصة

**المشكلة**: جداول Django غير موجودة في PostgreSQL
**الحل**: تشغيل `python manage.py migrate` على Render
**الطريقة الأسهل**: استخدام Shell من Render Dashboard

بعد تطبيق الحل، ستعمل الكوبونات بشكل صحيح على الإنتاج! 🎉