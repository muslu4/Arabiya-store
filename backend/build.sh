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
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

echo "✅ Build completed successfully!"
