# Generated by Django 4.1.1 on 2022-09-19 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_rename_products_cartitem_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='product',
            new_name='products',
        ),
    ]
