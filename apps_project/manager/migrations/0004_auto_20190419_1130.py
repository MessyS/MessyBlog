# Generated by Django 2.1.7 on 2019-04-19 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20190418_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daynumber',
            name='day',
            field=models.CharField(default='未知错误，记录默认时间2019-04-19 11:30:30', max_length=100),
        ),
        migrations.AlterField(
            model_name='goodboylist',
            name='time',
            field=models.DateTimeField(default='2019-04-19 11:30:30', verbose_name='时间'),
        ),
        migrations.AlterField(
            model_name='operatinghistory',
            name='time',
            field=models.DateTimeField(default='2019-04-19 11:30:30'),
        ),
        migrations.AlterField(
            model_name='userip',
            name='ip_address',
            field=models.CharField(default='0', max_length=200, verbose_name='IP地址归属地'),
        ),
        migrations.AlterField(
            model_name='userip',
            name='time',
            field=models.DateTimeField(default='2019-04-19 11:30:30'),
        ),
    ]
