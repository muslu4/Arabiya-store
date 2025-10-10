#!/bin/bash

# تثبيت المكتبات الأساسية
pip install --upgrade pip
pip install -r requirements.txt

# تثبيت مكتبات إضافية لدعم PostgreSQL
pip install psycopg psycopg-binary

# إنشاء الجداول مباشرة
chmod +x create_tables.sh
./create_tables.sh

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# تنفيذ الترحيلات
python manage.py migrate --noinput

# إنشاء مستخدم مدير إذا لم يكن موجودًا
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
