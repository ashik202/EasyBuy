# Generated by Django 4.1.1 on 2022-09-22 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='product',
            new_name='Product',
        ),
    ]