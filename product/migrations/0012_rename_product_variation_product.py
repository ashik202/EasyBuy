# Generated by Django 4.1.1 on 2022-09-25 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_rename_product_variation_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='Product',
            new_name='product',
        ),
    ]
