# Generated by Django 2.1.7 on 2019-04-16 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0006_auto_20190416_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mul',
            name='date_joined',
            field=models.CharField(default='2019-04-16 22-29-16', max_length=100, verbose_name='注册时间'),
        ),
        migrations.AlterField(
            model_name='mul',
            name='name',
            field=models.CharField(default='MessyXUiO_2916', max_length=100, verbose_name='用户名'),
        ),
    ]
