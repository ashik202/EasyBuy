# Generated by Django 4.1.1 on 2022-09-28 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_rename_product_variation_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=225, upload_to='store/products')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
