# Generated by Django 2.1.4 on 2019-03-13 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', '未指定')], default='N', max_length=10, verbose_name='性別'),
        ),
    ]
