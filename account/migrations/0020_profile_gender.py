# Generated by Django 2.1.4 on 2019-03-13 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20190223_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', '未指定')], default='M', max_length=10, verbose_name='性別'),
        ),
    ]
