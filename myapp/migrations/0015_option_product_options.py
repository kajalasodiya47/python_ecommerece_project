# Generated by Django 5.0.2 on 2024-03-24 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_remove_orderitem_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='options',
            field=models.ManyToManyField(blank=True, to='myapp.option'),
        ),
    ]
