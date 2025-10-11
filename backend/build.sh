#!/usr/bin/env bash
set -o errexit

echo "🚀 Starting build process..."

# تثبيت المتطلبات
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# ترحيل قاعدة البيانات
echo "🗄️ Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# جمع الملفات الثابتة
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# إنشاء جدول المستخدمين المخصص (إذا لم يكن موجودًا)
echo "👤 Creating superuser if needed..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(phone='01234567890', password='admin123', first_name='Admin', last_name='User') if not User.objects.filter(phone='01234567890').exists() else print('Superuser already exists')" | python manage.py shell

# إنشاء الكوبونات الافتراضية
echo "🎫 Creating default coupons..."
python create_coupons.py || echo "Coupons already exist or error occurred"

echo "✅ Build completed successfully!"
