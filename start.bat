@echo off
chcp 65001 >nul
echo 🚀 بدء تشغيل MIMI STORE...

REM Check if virtual environment exists
if not exist "backend\env" (
    echo 📦 إنشاء البيئة الافتراضية...
    cd backend
    python -m venv env
    cd ..
)

REM Activate virtual environment
echo 🔧 تفعيل البيئة الافتراضية...
call backend\env\Scripts\activate

REM Install backend dependencies
echo 📥 تثبيت متطلبات Backend...
pip install -r requirements.txt

REM Run migrations
echo 🗄️ تشغيل migrations...
python manage.py makemigrations users
python manage.py makemigrations products
python manage.py makemigrations orders
python manage.py migrate

REM Create admin user
echo 👤 إنشاء المستخدم الإداري (إذا لم يكن موجودًا)...
python create_admin_simple.py

REM Create sample data
echo 📊 إنشاء البيانات التجريبية...
python create_sample_data.py

REM Start backend server
echo 🖥️ تشغيل Backend server...
start "MIMI STORE Backend" cmd /k "backend\env\Scripts\python.exe manage.py runserver"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

echo.
echo ✅ تم تشغيل MIMI STORE Backend بنجاح!
echo.
echo 🔗 الروابط:
echo    Backend API: http://localhost:8000/api
echo    Django Admin: http://localhost:8000/admin
echo.
echo 👤 بيانات المشرف:
echo    الهاتف: admin
echo    كلمة المرور: admin123
echo.
echo 📱 اختبار API:
echo    المنتجات: http://localhost:8000/api/products/
echo    الأقسام: http://localhost:8000/api/products/categories/
echo.
echo  لإيقاف الخادم، أغلق نافذة Backend
echo.
pause