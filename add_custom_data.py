#!/usr/bin/env python3
"""
إضافة أقسام ومنتجات مخصصة لمتجر MIMI STORE
"""

import os
import sys
import django
from decimal import Decimal

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')
django.setup()

from products.models import Category, Product

def create_categories():
    """إنشاء أقسام جديدة"""
    
    categories_data = [
        {
            'name': 'أجهزة المنزل الذكي',
            'description': 'أجهزة ذكية لتحكم في المنزل والأتمتة'
        },
        {
            'name': 'الألعاب والترفيه',
            'description': 'ألعاب فيديو وأجهزة ترفيه'
        },
        {
            'name': 'الكاميرات والتصوير',
            'description': 'كاميرات رقمية ومعدات التصوير'
        },
        {
            'name': 'الصوتيات',
            'description': 'سماعات ومكبرات صوت عالية الجودة'
        },
        {
            'name': 'أجهزة الشحن والطاقة',
            'description': 'شواحن وبطاريات محمولة'
        }
    ]
    
    created_categories = []
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ تم إنشاء قسم: {category.name}")
        else:
            print(f"📂 القسم موجود مسبقاً: {category.name}")
        
        created_categories.append(category)
    
    return created_categories

def create_products_for_categories():
    """إنشاء منتجات للأقسام الجديدة"""
    
    # منتجات أجهزة المنزل الذكي
    smart_home_category = Category.objects.get(name='أجهزة المنزل الذكي')
    smart_home_products = [
        {
            'name': 'Amazon Echo Dot (5th Gen)',
            'description': 'مساعد صوتي ذكي مع Alexa',
            'price': Decimal('199.99'),
            'brand': 'Amazon',
            'stock_quantity': 50,
            'is_featured': True,
            'discount_percentage': 15
        },
        {
            'name': 'Philips Hue Smart Bulb',
            'description': 'مصباح LED ذكي قابل للتحكم عن بُعد',
            'price': Decimal('89.99'),
            'brand': 'Philips',
            'stock_quantity': 100,
            'is_featured': False,
            'discount_percentage': 10
        },
        {
            'name': 'Ring Video Doorbell',
            'description': 'جرس باب ذكي مع كاميرا وإنذار',
            'price': Decimal('299.99'),
            'brand': 'Ring',
            'stock_quantity': 25,
            'is_featured': True,
            'discount_percentage': 20
        }
    ]
    
    # منتجات الألعاب والترفيه
    gaming_category = Category.objects.get(name='الألعاب والترفيه')
    gaming_products = [
        {
            'name': 'PlayStation 5',
            'description': 'جهاز ألعاب سوني الجيل الخامس',
            'price': Decimal('1999.99'),
            'brand': 'Sony',
            'stock_quantity': 15,
            'is_featured': True,
            'discount_percentage': 5
        },
        {
            'name': 'Xbox Series X',
            'description': 'جهاز ألعاب مايكروسوفت الأقوى',
            'price': Decimal('1899.99'),
            'brand': 'Microsoft',
            'stock_quantity': 20,
            'is_featured': True,
            'discount_percentage': 8
        },
        {
            'name': 'Nintendo Switch OLED',
            'description': 'جهاز ألعاب محمول وثابت بشاشة OLED',
            'price': Decimal('1299.99'),
            'brand': 'Nintendo',
            'stock_quantity': 30,
            'is_featured': False,
            'discount_percentage': 12
        }
    ]
    
    # منتجات الكاميرات والتصوير
    camera_category = Category.objects.get(name='الكاميرات والتصوير')
    camera_products = [
        {
            'name': 'Canon EOS R6 Mark II',
            'description': 'كاميرا رقمية احترافية بدون مرآة',
            'price': Decimal('8999.99'),
            'brand': 'Canon',
            'stock_quantity': 10,
            'is_featured': True,
            'discount_percentage': 15
        },
        {
            'name': 'Sony Alpha A7 IV',
            'description': 'كاميرا فل فريم للمحترفين',
            'price': Decimal('9499.99'),
            'brand': 'Sony',
            'stock_quantity': 8,
            'is_featured': True,
            'discount_percentage': 10
        },
        {
            'name': 'GoPro HERO12 Black',
            'description': 'كاميرا أكشن مقاومة للماء 5.3K',
            'price': Decimal('1599.99'),
            'brand': 'GoPro',
            'stock_quantity': 40,
            'is_featured': False,
            'discount_percentage': 18
        }
    ]
    
    # منتجات الصوتيات
    audio_category = Category.objects.get(name='الصوتيات')
    audio_products = [
        {
            'name': 'Sony WH-1000XM5',
            'description': 'سماعات لاسلكية بإلغاء الضوضاء',
            'price': Decimal('1299.99'),
            'brand': 'Sony',
            'stock_quantity': 60,
            'is_featured': True,
            'discount_percentage': 20
        },
        {
            'name': 'Apple AirPods Pro (2nd Gen)',
            'description': 'سماعات أبل اللاسلكية مع إلغاء الضوضاء',
            'price': Decimal('999.99'),
            'brand': 'Apple',
            'stock_quantity': 80,
            'is_featured': True,
            'discount_percentage': 12
        },
        {
            'name': 'JBL Charge 5',
            'description': 'مكبر صوت محمول مقاوم للماء',
            'price': Decimal('599.99'),
            'brand': 'JBL',
            'stock_quantity': 45,
            'is_featured': False,
            'discount_percentage': 25
        }
    ]
    
    # منتجات أجهزة الشحن والطاقة
    power_category = Category.objects.get(name='أجهزة الشحن والطاقة')
    power_products = [
        {
            'name': 'Anker PowerCore 10000',
            'description': 'بطارية محمولة سريعة الشحن 10000mAh',
            'price': Decimal('149.99'),
            'brand': 'Anker',
            'stock_quantity': 100,
            'is_featured': False,
            'discount_percentage': 15
        },
        {
            'name': 'Apple MagSafe Charger',
            'description': 'شاحن لاسلكي مغناطيسي لآيفون',
            'price': Decimal('199.99'),
            'brand': 'Apple',
            'stock_quantity': 75,
            'is_featured': True,
            'discount_percentage': 8
        },
        {
            'name': 'Samsung 45W Super Fast Charger',
            'description': 'شاحن سريع 45 واط من سامسونج',
            'price': Decimal('129.99'),
            'brand': 'Samsung',
            'stock_quantity': 90,
            'is_featured': False,
            'discount_percentage': 20
        }
    ]
    
    # دمج جميع المنتجات
    all_products = [
        (smart_home_category, smart_home_products),
        (gaming_category, gaming_products),
        (camera_category, camera_products),
        (audio_category, audio_products),
        (power_category, power_products)
    ]
    
    created_count = 0
    
    for category, products in all_products:
        print(f"\n📂 إضافة منتجات لقسم: {category.name}")
        
        for product_data in products:
            # حساب السعر بعد الخصم
            original_price = product_data['price']
            discount = product_data.get('discount_percentage', 0)
            discounted_price = original_price * (1 - Decimal(discount) / 100)
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'category': category,
                    'description': product_data['description'],
                    'price': original_price,
                    'discounted_price': discounted_price if discount > 0 else None,
                    'discount_percentage': discount if discount > 0 else None,
                    'brand': product_data['brand'],
                    'stock_quantity': product_data['stock_quantity'],
                    'is_active': True,
                    'is_featured': product_data['is_featured']
                }
            )
            
            if created:
                print(f"  ✅ {product.name} - {original_price} ريال")
                if discount > 0:
                    print(f"     💰 خصم {discount}% - السعر بعد الخصم: {discounted_price:.2f} ريال")
                created_count += 1
            else:
                print(f"  📦 {product.name} - موجود مسبقاً")
    
    return created_count

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء إضافة أقسام ومنتجات جديدة لمتجر MIMI STORE...")
    print("=" * 60)
    
    try:
        # إنشاء الأقسام
        print("📂 إنشاء الأقسام الجديدة...")
        categories = create_categories()
        
        print(f"\n✅ تم إنشاء {len(categories)} أقسام")
        
        # إنشاء المنتجات
        print("\n📦 إنشاء المنتجات...")
        products_count = create_products_for_categories()
        
        print(f"\n🎉 تم الانتهاء بنجاح!")
        print(f"📊 الإحصائيات:")
        print(f"   - الأقسام: {Category.objects.count()} قسم")
        print(f"   - المنتجات: {Product.objects.count()} منتج")
        print(f"   - المنتجات الجديدة: {products_count} منتج")
        
        print(f"\n🌐 يمكنك الآن مشاهدة الأقسام والمنتجات الجديدة في:")
        print(f"   - الواجهة الأمامية: http://localhost:3000")
        print(f"   - لوحة الإدارة: http://localhost:8000/admin")
        print(f"   - API الأقسام: http://localhost:8000/api/products/categories/")
        print(f"   - API المنتجات: http://localhost:8000/api/products/")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✨ تم إضافة البيانات بنجاح!")
    else:
        print("\n💥 فشل في إضافة البيانات!")
    
    input("\nاضغط Enter للخروج...")