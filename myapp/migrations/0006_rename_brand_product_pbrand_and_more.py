# Generated by Django 5.0.2 on 2024-02-29 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='brand',
            new_name='pbrand',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='pcategory',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='size',
            new_name='psize',
        ),
        migrations.AlterField(
            model_name='product',
            name='ppicture',
            field=models.ImageField(default='', upload_to='ppicture/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
