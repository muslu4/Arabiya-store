#!/bin/bash

# تثبيت المكتبات الأساسية
pip install --upgrade pip
pip install -r requirements.txt

# تثبيت مكتبات إضافية لدعم PostgreSQL
pip install psycopg psycopg-binary

# إنشاء الجداول مباشرة
python create_tables.py

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# تنفيذ الترحيلات
python manage.py migrate --noinput

# إنشاء مستخدم مدير إذا لم يكن موجودًا
python create_superuser.py
