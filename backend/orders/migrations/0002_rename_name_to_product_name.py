
# Generated migration to rename 'name' field to 'product_name'

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='name',
            new_name='product_name',
        ),
    ]
