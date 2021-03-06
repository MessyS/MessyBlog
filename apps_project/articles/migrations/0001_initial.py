# Generated by Django 2.1.7 on 2019-04-18 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('oauth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('time', models.DateTimeField(default='2019-04-18 09:02:57')),
                ('photo', models.CharField(default='/media/defaultPhotos/25.jpg', max_length=800)),
                ('context', models.TextField(default='内容死掉了.....(▼ヘ▼#)')),
                ('front_context', models.TextField(default='内容死掉了.....(▼ヘ▼#)')),
                ('traffic', models.PositiveIntegerField(default=0, null=True)),
                ('comments', models.PositiveIntegerField(default=0, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='oauth.MUL')),
            ],
            options={
                'verbose_name': '文章详情页',
                'verbose_name_plural': '文章详情页',
                'ordering': ['-time'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '文章分类表',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorys1', to='articles.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='category2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categorys2', to='articles.Category'),
        ),
    ]
