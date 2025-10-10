# Generated migration for coupons

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='كود الكوبون')),
                ('description', models.TextField(blank=True, verbose_name='وصف الكوبون')),
                ('discount_type', models.CharField(choices=[('percentage', 'نسبة مئوية'), ('fixed', 'قيمة ثابتة')], default='percentage', max_length=10, verbose_name='نوع الخصم')),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='قيمة الخصم')),
                ('minimum_order_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='الحد الأدنى للطلب')),
                ('max_discount_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='الحد الأقصى للخصم')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاريخ البدء')),
                ('end_date', models.DateTimeField(verbose_name='تاريخ الانتهاء')),
                ('usage_limit', models.PositiveIntegerField(blank=True, null=True, verbose_name='حد الاستخدام')),
                ('used_count', models.PositiveIntegerField(default=0, verbose_name='عدد مرات الاستخدام')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
            ],
            options={
                'verbose_name': 'كوبون الخصم',
                'verbose_name_plural': 'كوبونات الخصم',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CouponUsage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('discount_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='قيمة الخصم')),
                ('used_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الاستخدام')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.coupon', verbose_name='الكوبون')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='الطلب')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='المستخدم')),
            ],
            options={
                'verbose_name': 'استخدام الكوبون',
                'verbose_name_plural': 'استخدامات الكوبون',
                'ordering': ['-used_at'],
                'unique_together': {('coupon', 'order')},
            },
        ),
    ]
