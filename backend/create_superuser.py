#!/usr/bin/env python
"""Create superuser if it doesn't exist"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(phone='01234567890').exists():
    User.objects.create_superuser(
        phone='01234567890',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Superuser created successfully!')
else:
    print('ℹ️ Superuser already exists')