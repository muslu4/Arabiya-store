#!/usr/bin/env python
"""
Create superuser with phone number
"""
import os
import sys
import django

def create_superuser():
    """
    Create superuser with phone number
    """
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Check if user already exists
        if User.objects.filter(phone='01234567890').exists():
            print("Superuser already exists!")
            return True

        # Create superuser
        user = User.objects.create_superuser(
            phone='01234567890',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )

        print(f"Superuser created successfully with phone: {user.phone}")
        return True

    except Exception as e:
        print(f"Error creating superuser: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Configure Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')

    try:
        django.setup()
        create_superuser()
    except Exception as e:
        print(f"Error setting up Django: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
