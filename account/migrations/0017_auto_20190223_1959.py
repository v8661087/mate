# Generated by Django 2.1.4 on 2019-02-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20190223_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank='users/default.jpg', default='users/default.jpg', null='users/default.jpg', upload_to='users/%Y/%m/%d'),
        ),
    ]
