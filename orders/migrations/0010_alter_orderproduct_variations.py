# Generated by Django 4.1.1 on 2022-09-26 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_rename_product_variation_product'),
        ('orders', '0009_alter_order_order_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, default=True, to='product.variation'),
        ),
    ]
