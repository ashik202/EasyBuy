# Generated by Django 4.1.1 on 2022-09-23 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_variation_variation_category'),
        ('cart', '0004_rename_product_cartitem_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='product.variation'),
        ),
    ]
