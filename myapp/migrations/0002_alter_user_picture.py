# Generated by Django 5.0.2 on 2024-02-19 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='default.png', upload_to='profile/'),
        ),
    ]
