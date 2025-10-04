
import os
import django
from django.core.files import File
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')
django.setup()

from products.models import Product, Category

# Create categories
categories = [
    {"name": "هواتف ذكية", "description": "أحدث الهواتف الذكية"},
    {"name": "لابتوبات", "description": "أجهزة الكمبيوتر المحمولة"},
    {"name": "إكسسوارات", "description": "إكسسوارات الهواتف والأجهزة الإلكترونية"},
]

for cat_data in categories:
    Category.objects.get_or_create(
        name=cat_data["name"],
        defaults={"description": cat_data["description"]}
    )

# Create products
products = [
    {
        "name": "iPhone 13",
        "description": "أحدث هاتف من آبل",
        "price": 500000,
        "category": Category.objects.get(name="هواتف ذكية"),
        "stock_quantity": 10,
    },
    {
        "name": "MacBook Pro",
        "description": "لابتوب احترافي",
        "price": 1500000,
        "category": Category.objects.get(name="لابتوبات"),
        "stock_quantity": 5,
    },
    {
        "name": "ايربود",
        "description": "سماعات لاسلكية",
        "price": 120,
        "category": Category.objects.get(name="إكسسوارات"),
        "stock_quantity": 100,
    },
]

for prod_data in products:
    Product.objects.get_or_create(
        name=prod_data["name"],
        defaults=prod_data
    )

print("Sample data created successfully!")
