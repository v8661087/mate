# Generated by Django 2.1.4 on 2019-03-27 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_auto_20190325_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.URLField(blank=True, default='https://raw.githubusercontent.com/v8661087/v8661087.github.io/master/media/users/default.jpg'),
        ),
    ]