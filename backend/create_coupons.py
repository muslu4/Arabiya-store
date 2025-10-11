#!/usr/bin/env python
"""
سكريبت لإنشاء الكوبونات الافتراضية
"""
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')
django.setup()

from products.models import Coupon

def create_coupons():
    """إنشاء الكوبونات الافتراضية"""
    
    coupons_data = [
        {
            'code': 'VIP15',
            'discount_type': 'percentage',
            'discount_value': 15.00,
            'minimum_order_amount': 100.00,
            'usage_limit': 100,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=90),
            'is_active': True,
            'description': 'خصم 15% للعملاء المميزين'
        },
        {
            'code': 'SUMMER50',
            'discount_type': 'fixed',
            'discount_value': 50.00,
            'minimum_order_amount': 200.00,
            'usage_limit': 50,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=60),
            'is_active': True,
            'description': 'خصم 50 دينار على المشتريات فوق 200 دينار'
        },
        {
            'code': 'SPECIAL25',
            'discount_type': 'percentage',
            'discount_value': 25.00,
            'minimum_order_amount': 150.00,
            'usage_limit': 30,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=45),
            'is_active': True,
            'description': 'خصم 25% للعروض الخاصة'
        },
        {
            'code': 'SAVE20',
            'discount_type': 'percentage',
            'discount_value': 20.00,
            'minimum_order_amount': 80.00,
            'usage_limit': 200,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=120),
            'is_active': True,
            'description': 'وفر 20% على مشترياتك'
        },
        {
            'code': 'WELCOME10',
            'discount_type': 'percentage',
            'discount_value': 10.00,
            'minimum_order_amount': 50.00,
            'usage_limit': 500,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=180),
            'is_active': True,
            'description': 'خصم ترحيبي 10% للعملاء الجدد'
        },
        {
            'code': 'TEST2024',
            'discount_type': 'percentage',
            'discount_value': 5.00,
            'minimum_order_amount': 30.00,
            'usage_limit': 1000,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=365),
            'is_active': True,
            'description': 'كوبون تجريبي 5%'
        },
    ]
    
    created_count = 0
    updated_count = 0
    
    for coupon_data in coupons_data:
        code = coupon_data['code']
        coupon, created = Coupon.objects.update_or_create(
            code=code,
            defaults=coupon_data
        )
        
        if created:
            created_count += 1
            print(f"✅ تم إنشاء الكوبون: {code}")
        else:
            updated_count += 1
            print(f"🔄 تم تحديث الكوبون: {code}")
    
    print(f"\n📊 الملخص:")
    print(f"   - تم إنشاء: {created_count} كوبون")
    print(f"   - تم تحديث: {updated_count} كوبون")
    print(f"   - المجموع: {created_count + updated_count} كوبون")
    
    return created_count, updated_count

if __name__ == '__main__':
    print("🚀 بدء إنشاء الكوبونات...\n")
    create_coupons()
    print("\n✅ تم الانتهاء!")