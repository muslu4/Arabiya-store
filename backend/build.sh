#!/bin/bash

# تثبيت المتطلبات
pip install -r requirements.txt

# ترحيل قاعدة البيانات
python manage.py makemigrations
python manage.py migrate

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# إنشاء جدول المستخدمين المخصص (إذا لم يكن موجودًا)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
