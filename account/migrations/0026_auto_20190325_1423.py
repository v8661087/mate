# Generated by Django 2.1.4 on 2019-03-25 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_auto_20190325_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='users/default.jpg', upload_to='users/%Y/%m/%d'),
        ),
    ]
