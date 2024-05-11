# Generated by Django 5.0.2 on 2024-03-18 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_rename_product_price_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
