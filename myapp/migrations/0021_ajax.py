# Generated by Django 5.0.2 on 2024-03-28 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_remove_orderitem_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ajax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=20)),
                ('mobile', models.PositiveBigIntegerField()),
            ],
        ),
    ]
