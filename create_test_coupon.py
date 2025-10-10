#!/usr/bin/env python
"""
Create test coupon
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')
django.setup()

from products.models_coupons import Coupon

def create_test_coupon():
    """
    Create test coupon
    """
    print("Creating test coupon...")

    try:
        # Create test coupon
        coupon = Coupon.objects.create(
            code='TEST10',
            description='خصم 10% على جميع المنتجات',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            minimum_order_amount=Decimal('50.00'),
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
            usage_limit=100,
            is_active=True
        )

        print(f"Created coupon: {coupon.code}")
        print(f"Discount: {coupon.discount_value}%")
        print(f"Valid until: {coupon.end_date}")

        return True

    except Exception as e:
        print(f"Error creating coupon: {e}")
        return False

if __name__ == '__main__':
    create_test_coupon()
