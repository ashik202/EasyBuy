# Generated by Django 4.1.1 on 2022-09-24 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_variation_variation_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='Product',
            new_name='product',
        ),
        migrations.AddField(
            model_name='variation',
            name='color_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='variation',
            name='created_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_value',
            field=models.CharField(max_length=7),
        ),
    ]