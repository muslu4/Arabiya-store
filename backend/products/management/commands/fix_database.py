from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create missing coupon-related tables in the database'

    def handle(self, *args, **options):
        self.stdout.write('Creating missing coupon-related tables...')

        try:
            with connection.cursor() as cursor:
                # Create products_coupon table if it doesn't exist
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS products_coupon (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code VARCHAR(50) NOT NULL UNIQUE,
                    description TEXT,
                    discount_type VARCHAR(20) NOT NULL,
                    discount_value DECIMAL(10, 2) NOT NULL,
                    minimum_amount DECIMAL(10, 2) DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    usage_limit INTEGER,
                    used_count INTEGER DEFAULT 0,
                    valid_from DATETIME,
                    valid_until DATETIME,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
                """)
                self.stdout.write(self.style.SUCCESS('Created products_coupon table'))

                # Create products_coupon_excluded_products table if it doesn't exist
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS products_coupon_excluded_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    coupon_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    UNIQUE(coupon_id, product_id)
                )
                """)
                self.stdout.write(self.style.SUCCESS('Created products_coupon_excluded_products table'))

                # Create products_coupon_excluded_categories table if it doesn't exist
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS products_coupon_excluded_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    coupon_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    UNIQUE(coupon_id, category_id)
                )
                """)
                self.stdout.write(self.style.SUCCESS('Created products_coupon_excluded_categories table'))

                # Create products_couponusage table if it doesn't exist
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS products_couponusage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    coupon_id INTEGER NOT NULL,
                    order_id INTEGER,
                    used_at DATETIME NOT NULL
                )
                """)
                self.stdout.write(self.style.SUCCESS('Created products_couponusage table'))

            self.stdout.write(self.style.SUCCESS('Database tables created successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating tables: {str(e)}'))
