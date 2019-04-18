from django.db import models
import time,random,string

#常用变量
nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
randomPhoto = "<div class='g-body-branch-photo-bgi' style='background: url(/media/defaultPhotos/%s.jpg)'></div>" \
              % round(random.random() * 36)

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '文章分类表'

class Article(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField(default=nowTime)
    photo = models.CharField(max_length=800,default=randomPhoto)
    context = models.TextField(default='内容死掉了.....(▼ヘ▼#)')
    front_context = models.TextField(default='内容死掉了.....(▼ヘ▼#)')
    author = models.ForeignKey('oauth.MUL',on_delete=models.CASCADE,related_name='authors')
    category1 = models.ForeignKey('Category', on_delete=models.CASCADE,related_name='categorys1')
    category2 = models.ForeignKey('Category', on_delete=models.CASCADE,related_name='categorys2',null=True)
    traffic = models.PositiveIntegerField(null=True,default=0)
    comments = models.PositiveIntegerField(null=True,default=0)

    class Meta:
        ordering = ['-time']
        verbose_name = '文章详情页'
        verbose_name_plural = verbose_name