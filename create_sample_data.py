#!/usr/bin/env python
"""
Script to create sample data for MIMI STORE
"""
import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')
django.setup()

from products.models import Category, Product
from users.models import User
from decimal import Decimal

def create_sample_data():
    print("Creating sample data for MIMI STORE...")
    
    # Create admin user first
    print("Creating admin user...")
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'phone': 'admin',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Admin user created successfully")
        print("   Phone: admin")
        print("   Password: admin123")
    else:
        print("Admin user already exists")
    
    # Create categories
    categories_data = [
        {
            'name': 'Smartphones',
            'description': 'Latest smartphones and accessories'
        },
        {
            'name': 'Tablets',
            'description': 'A variety of tablets for work and entertainment'
        },
        {
            'name': 'Computers',
            'description': 'Laptops and desktops'
        },
        {
            'name': 'Accessories',
            'description': 'Electronic accessories and peripherals'
        },
        {
            'name': 'Smart Watches',
            'description': 'Smart watches and wearable devices'
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = category
        if created:
            print(f"Category created: {category.name}")
    
    # Create products
    products_data = [
        # Smartphones
        {
            'name': 'iPhone 15 Pro Max',
            'description': 'The latest phone from Apple with advanced technologies and a professional camera',
            'category': 'Smartphones',
            'price': Decimal('4999.00'),
            'discount_percentage': 10,
            'stock_quantity': 25,
            'brand': 'Apple',
            'model': 'iPhone 15 Pro Max',
            'color': 'Natural Titanium',
            'is_featured': True,
            'tags': 'iPhone, Apple, smartphone, professional camera',
            'main_image': 'https://via.placeholder.com/300'
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'description': 'Samsung\'s flagship phone with S Pen and 200MP camera',
            'category': 'Smartphones',
            'price': Decimal('4299.00'),
            'discount_percentage': 15,
            'stock_quantity': 30,
            'brand': 'Samsung',
            'model': 'Galaxy S24 Ultra',
            'color': 'Titanium Black',
            'is_featured': True,
            'tags': 'Samsung, Galaxy, smartphone, S Pen',
            'main_image': 'https://via.placeholder.com/300'
        },
        {
            'name': 'Xiaomi 14 Pro',
            'description': 'Xiaomi phone with Snapdragon 8 Gen 3 processor and fast charging',
            'category': 'Smartphones',
            'price': Decimal('2799.00'),
            'discount_percentage': 20,
            'stock_quantity': 40,
            'brand': 'Xiaomi',
            'model': '14 Pro',
            'color': 'White',
            'is_featured': False,
            'tags': 'Xiaomi, smartphone, fast charging',
            'main_image': 'https://via.placeholder.com/300'
        },
        
        # Tablets
        {
            'name': 'iPad Pro 12.9 M2',
            'description': 'Apple\'s professional tablet with M2 chip and Liquid Retina XDR display',
            'category': 'Tablets',
            'price': Decimal('3999.00'),
            'discount_percentage': 5,
            'stock_quantity': 15,
            'brand': 'Apple',
            'model': 'iPad Pro 12.9',
            'color': 'Space Gray',
            'is_featured': True,
            'tags': 'iPad, Apple, tablet, M2',
            'main_image': 'https://via.placeholder.com/300'
        },
        {
            'name': 'Samsung Galaxy Tab S9 Ultra',
            'description': 'Samsung\'s large tablet with a 14.6-inch screen and S Pen',
            'category': 'Tablets',
            'price': Decimal('3499.00'),
            'discount_percentage': 12,
            'stock_quantity': 20,
            'brand': 'Samsung',
            'model': 'Galaxy Tab S9 Ultra',
            'color': 'Beige',
            'is_featured': False,
            'tags': 'Samsung, tablet, S Pen',
            'main_image': 'https://via.placeholder.com/300'
        },
        
        # Laptops
        {
            'name': 'MacBook Pro 16 M3 Pro',
            'description': 'Apple\'s professional laptop with M3 Pro chip and Liquid Retina XDR display',
            'category': 'Computers',
            'price': Decimal('8999.00'),
            'discount_percentage': 8,
            'stock_quantity': 10,
            'brand': 'Apple',
            'model': 'MacBook Pro 16',
            'color': 'Space Gray',
            'is_featured': True,
            'tags': 'MacBook, Apple, laptop, M3 Pro',
            'main_image': 'https://via.placeholder.com/300'
        },
        {
            'name': 'Dell XPS 15',
            'description': 'Dell\'s professional laptop with Intel Core i7 processor and RTX 4060 graphics card',
            'category': 'Computers',
            'price': Decimal('6499.00'),
            'discount_percentage': 10,
            'stock_quantity': 12,
            'brand': 'Dell',
            'model': 'XPS 15',
            'color': 'Silver',
            'is_featured': False,
            'tags': 'Dell, laptop, Intel, RTX',
            'main_image': 'https://via.placeholder.com/300'
        },
        
        # Accessories
        {
            'name': 'AirPods Pro 2',
            'description': 'Apple\'s wireless earbuds with active noise cancellation',
            'category': 'Accessories',
            'price': Decimal('899.00'),
            'discount_percentage': 15,
            'stock_quantity': 50,
            'brand': 'Apple',
            'model': 'AirPods Pro 2',
            'color': 'White',
            'is_featured': True,
            'tags': 'AirPods, Apple, wireless earbuds',
            'main_image': 'https://via.placeholder.com/300'
        },
        {
            'name': 'Fast Wireless Charger',
            'description': '15W fast wireless charger compatible with all devices',
            'category': 'Accessories',
            'price': Decimal('199.00'),
            'discount_percentage': 25,
            'stock_quantity': 100,
            'brand': 'Generic',
            'model': 'Wireless Charger 15W',
            'color': 'Black',
            'is_featured': False,
            'tags': 'wireless charger, fast charging',
            'main_image': 'https://via.placeholder.com/300'
        },
        
        # Smart Watches
        {
            'name': 'Apple Watch Series 9',
            'description': 'The new Apple Watch with S9 chip and advanced health features',
            'category': 'Smart Watches',
            'price': Decimal('1599.00'),
            'discount_percentage': 12,
            'stock_quantity': 35,
            'brand': 'Apple',
            'model': 'Watch Series 9',
            'color': 'Red',
            'is_featured': True,
            'tags': 'Apple Watch, smart watch, health',
            'main_image': 'https://via.placeholder.com/300'
        },
        {
            'name': 'Samsung Galaxy Watch 6',
            'description': 'Samsung\'s smart watch with Wear OS and comprehensive health monitoring',
            'category': 'Smart Watches',
            'price': Decimal('1299.00'),
            'discount_percentage': 18,
            'stock_quantity': 25,
            'brand': 'Samsung',
            'model': 'Galaxy Watch 6',
            'color': 'Gold',
            'is_featured': False,
            'tags': 'Samsung, smart watch, Wear OS',
            'main_image': 'https://via.placeholder.com/300'
        }
    ]
    
    for product_data in products_data:
        category_name = product_data.pop('category')
        category = categories[category_name]
        
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': category,
                **product_data
            }
        )
        
        if created:
            print(f"Product created: {product.name}")
    
    print(f"\nSample data created successfully!")
    print(f"Statistics:")
    print(f"   - Categories: {Category.objects.count()}")
    print(f"   - Products: {Product.objects.count()}")
    print(f"   - Users: {User.objects.count()}")
    
    print(f"\nLogin credentials:")
    print(f"   - Phone: admin")
    print(f"   - Password: admin123")
    
    print(f"\nLinks:")
    print(f"   - Backend API: http://localhost:8000/api")
    print(f"   - Django Admin: http://localhost:8000/admin")

if __name__ == '__main__':
    create_sample_data()