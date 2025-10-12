# Generated migration to change discount from percentage to amount

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_main_image_alter_product_image_2_and_more'),
    ]

    operations = [
        # إضافة حقل جديد للخصم بالمبلغ
        migrations.AddField(
            model_name='product',
            name='discount_amount',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text='أدخل مبلغ الخصم بالدينار العراقي (مثال: 2000 لخصم 2000 د.ع)',
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name='مبلغ الخصم (د.ع)'
            ),
        ),
        # تحويل القيم القديمة من نسبة إلى مبلغ
        migrations.RunPython(
            code=lambda apps, schema_editor: convert_discount_percentage_to_amount(apps, schema_editor),
            reverse_code=migrations.RunPython.noop,
        ),
        # حذف الحقل القديم
        migrations.RemoveField(
            model_name='product',
            name='discount_percentage',
        ),
    ]


def convert_discount_percentage_to_amount(apps, schema_editor):
    """تحويل نسبة الخصم إلى مبلغ"""
    Product = apps.get_model('products', 'Product')
    
    for product in Product.objects.all():
        if hasattr(product, 'discount_percentage') and product.discount_percentage > 0:
            # حساب مبلغ الخصم من النسبة
            discount_amount = (product.price * product.discount_percentage) / 100
            product.discount_amount = discount_amount
            product.save(update_fields=['discount_amount'])