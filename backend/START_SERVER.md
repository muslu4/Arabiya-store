# كيفية تشغيل خادم Django

## الخطوات

### 1. تأكد من أن Terminal في المجلد الصحيح

```bash
cd c:\Users\a\Desktop\ecom_setup\ecom_project\ecom_project\backend
```

### 2. (اختياري) قم بتشغيل الفحص النهائي

```bash
python final_check.py
```

يجب أن ترى:
```
✅ جميع الفحوصات نجحت!
```

### 3. شغل خادم Django

```bash
python manage.py runserver
```

يجب أن ترى:
```
Starting development server at http://127.0.0.1:8000/
```

### 4. افتح المتصفح

اذهب إلى:
```
http://127.0.0.1:8000/admin/
```

### 5. سجل الدخول

```
Username: admin
Password: admin123
```

## إذا واجهت مشاكل

### المشكلة: "Port already in use"

**الحل:**
```bash
# أوقف الخادم القديم أولاً (Ctrl+C)
# أو استخدم port آخر:
python manage.py runserver 8001
```

### المشكلة: "Cannot force an update in save() with no primary key"

**الحل:**
```bash
# أوقف الخادم (Ctrl+C)
# شغل سكريبت الإصلاح:
python fix_all_tables.py

# نظف الجلسات:
python clear_sessions.py

# شغل الخادم مرة أخرى:
python manage.py runserver
```

### المشكلة: "No such table: users_user"

**الحل:**
```bash
python manage.py migrate
```

## ملاحظات

- ✅ تم إصلاح مشكلة Primary Key
- ✅ تم تعطيل إنشاء الجداول التلقائي
- ✅ جميع الجداول تستخدم SQLite syntax الصحيح
- ✅ المستخدم الإداري جاهز (admin/admin123)

## للمزيد من المعلومات

اقرأ ملف `FIX_SUMMARY.md` للحصول على تفاصيل كاملة عن الإصلاحات.