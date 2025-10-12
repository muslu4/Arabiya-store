#!/usr/bin/env bash
set -o errexit

echo "🚀 Starting backend build process..."

# تثبيت المتطلبات
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# ترحيل قاعدة البيانات - FORCE IT!
echo "🗄️ FORCING database migrations..."
python manage.py makemigrations --noinput || echo "No new migrations"
python manage.py migrate --noinput --run-syncdb

# جمع الملفات الثابتة
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# إنشاء المستخدم الإداري
echo "👤 Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(phone='01234567890').exists():
    User.objects.create_superuser(
        phone='01234567890',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Superuser created!')
else:
    print('ℹ️ Superuser already exists')
EOF

# إنشاء الكوبونات
echo "🎫 Creating default coupons..."
python manage.py shell << EOF
import os
import django
from datetime import datetime, timedelta
from products.models import Coupon

coupons_data = [
    {'code': 'VIP15', 'discount_type': 'percentage', 'discount_value': 15.00, 'minimum_order_amount': 100.00, 'usage_limit': 100, 'start_date': datetime.now(), 'end_date': datetime.now() + timedelta(days=90), 'is_active': True, 'description': 'خصم 15% للعملاء المميزين'},
    {'code': 'SUMMER50', 'discount_type': 'fixed', 'discount_value': 50.00, 'minimum_order_amount': 200.00, 'usage_limit': 50, 'start_date': datetime.now(), 'end_date': datetime.now() + timedelta(days=60), 'is_active': True, 'description': 'خصم 50 دينار'},
    {'code': 'SPECIAL25', 'discount_type': 'percentage', 'discount_value': 25.00, 'minimum_order_amount': 150.00, 'usage_limit': 30, 'start_date': datetime.now(), 'end_date': datetime.now() + timedelta(days=45), 'is_active': True, 'description': 'خصم 25%'},
    {'code': 'SAVE20', 'discount_type': 'percentage', 'discount_value': 20.00, 'minimum_order_amount': 80.00, 'usage_limit': 200, 'start_date': datetime.now(), 'end_date': datetime.now() + timedelta(days=120), 'is_active': True, 'description': 'وفر 20%'},
    {'code': 'WELCOME10', 'discount_type': 'percentage', 'discount_value': 10.00, 'minimum_order_amount': 50.00, 'usage_limit': 500, 'start_date': datetime.now(), 'end_date': datetime.now() + timedelta(days=180), 'is_active': True, 'description': 'خصم ترحيبي 10%'},
    {'code': 'TEST2024', 'discount_type': 'percentage', 'discount_value': 5.00, 'minimum_order_amount': 30.00, 'usage_limit': 1000, 'start_date': datetime.now(), 'end_date': datetime.now() + timedelta(days=365), 'is_active': True, 'description': 'كوبون تجريبي 5%'},
]

for coupon_data in coupons_data:
    code = coupon_data['code']
    coupon, created = Coupon.objects.update_or_create(code=code, defaults=coupon_data)
    if created:
        print(f'✅ Created coupon: {code}')
    else:
        print(f'ℹ️ Updated coupon: {code}')

print('✅ All coupons ready!')
EOF

echo "✅ Backend build completed successfully!"
