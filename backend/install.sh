#!/usr/bin/env bash
set -o errexit

echo "🚀 Starting backend build process..."

# تثبيت المتطلبات
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# ترحيل قاعدة البيانات - FORCE IT!
echo "🗄️ FORCING database migrations..."
python manage.py makemigrations --noinput || echo "⚠️ No new migrations to create"
echo "🔄 Running migrate with --run-syncdb..."
python manage.py migrate --noinput --run-syncdb || {
    echo "❌ Migration failed! Trying without --run-syncdb..."
    python manage.py migrate --noinput
}

# جمع الملفات الثابتة
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# إنشاء المستخدم الإداري
echo "👤 Creating superuser..."
python create_superuser.py || echo "⚠️ Superuser creation failed (might already exist)"

# إنشاء الكوبونات
echo "🎫 Creating default coupons..."
python create_coupons.py || echo "⚠️ Coupon creation failed (might already exist)"

echo "✅ Backend build completed successfully!"
