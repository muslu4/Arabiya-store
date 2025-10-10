# 🚀 دليل البدء السريع - MIMI STORE

## التشغيل السريع (Windows)

1. **تشغيل تلقائي:**
   ```bash
   # انقر مرتين على الملف
   start.bat
   ```

2. **تشغيل يدوي:**
   ```bash
   # Backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   
   # Frontend (في terminal جديد)
   cd frontend
   npm install
   npm start
   ```

## التشغيل السريع (Mac/Linux)

```bash
# اجعل الملف قابل للتنفيذ
chmod +x start.sh

# تشغيل
./start.sh
```

## الروابط المهمة

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Admin Panel:** http://localhost:3000/admin-panel
- **Django Admin:** http://localhost:8000/admin

## بيانات الدخول الافتراضية

- **الهاتف:** admin
- **كلمة المرور:** admin123

## إعداد Firebase (مطلوب للإشعارات)

1. اذهب إلى [Firebase Console](https://console.firebase.google.com/)
2. أنشئ مشروع جديد
3. فعّل Cloud Messaging
4. احصل على ملف `firebase-credentials.json`
5. ضعه في المجلد الجذر
6. أضف إعدادات Firebase في `.env`

## إعداد Cloudinary (مطلوب لرفع الصور)

1. اذهب إلى [Cloudinary](https://cloudinary.com/)
2. أنشئ حساب مجاني
3. احصل على Cloud Name, API Key, API Secret
4. أنشئ Upload Preset (unsigned)
5. أضف الإعدادات في `.env`

## الملفات المطلوبة

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
FIREBASE_PROJECT_ID=your-project-id
CLOUDINARY_CLOUD_NAME=your-cloud-name
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_CLOUDINARY_CLOUD_NAME=your-cloud-name
```

## المميزات الجاهزة

✅ تسجيل المستخدمين برقم الهاتف  
✅ JWT Authentication  
✅ إدارة المنتجات والأقسام  
✅ سلة التسوق  
✅ نظام الطلبات  
✅ لوحة إدارة متقدمة  
✅ إشعارات Firebase  
✅ رفع الصور على Cloudinary  
✅ تصميم عربي متجاوب  
✅ PWA جاهز  

## استكشاف الأخطاء

### خطأ في قاعدة البيانات
```bash
python manage.py makemigrations
python manage.py migrate
```

### خطأ في المتطلبات
```bash
pip install -r requirements.txt
```

### خطأ في Frontend
```bash
cd frontend
npm install
npm start
```

### خطأ CORS
تأكد من إضافة `http://localhost:3000` في `CORS_ALLOWED_ORIGINS`

## النشر السريع

### Render (Backend)
1. ارفع الكود على GitHub
2. اربط مع Render
3. أضف متغيرات البيئة
4. انشر

### Netlify (Frontend)
1. ارفع مجلد frontend على GitHub
2. اربط مع Netlify
3. أضف متغيرات البيئة
4. انشر

## الدعم

للمساعدة، راجع:
- `README.md` للتفاصيل الكاملة
- سجلات الأخطاء في Terminal
- إعدادات Firebase و Cloudinary

---
**تم إنشاء هذا المشروع بـ ❤️ للمطورين العرب**