# Generated by Django 2.1.4 on 2019-04-07 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0019_auto_20190327_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='slug',
        ),
    ]
