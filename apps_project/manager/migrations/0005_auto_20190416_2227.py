# Generated by Django 2.1.7 on 2019-04-16 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20190416_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daynumber',
            name='day',
            field=models.CharField(default='未知错误，记录默认时间2019-04-16 22:27:35', max_length=100),
        ),
        migrations.AlterField(
            model_name='goodboylist',
            name='time',
            field=models.CharField(default='2019-04-16 22:27:35', max_length=100, verbose_name='时间'),
        ),
        migrations.AlterField(
            model_name='operatinghistory',
            name='time',
            field=models.CharField(default='2019-04-16 22:27:35', max_length=100),
        ),
        migrations.AlterField(
            model_name='userip',
            name='time',
            field=models.CharField(default='2019-04-16 22:27:35', max_length=100),
        ),
    ]
