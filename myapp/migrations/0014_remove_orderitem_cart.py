# Generated by Django 5.0.2 on 2024-03-22 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_orderitem_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='cart',
        ),
    ]
