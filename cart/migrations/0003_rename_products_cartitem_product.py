# Generated by Django 4.1.1 on 2022-09-19 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_product_cartitem_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='products',
            new_name='product',
        ),
    ]