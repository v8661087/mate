# Generated by Django 2.1.4 on 2019-02-23 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20190223_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='users/default.jpg', null=True, upload_to='users/%Y/%m/%d'),
        ),
    ]
