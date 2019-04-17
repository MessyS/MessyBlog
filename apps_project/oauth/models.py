from django.db import models
import time,random,string

#常用变量
now_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
now_time_s = time.strftime('%M%S', time.localtime(time.time()))
random_str = ''.join(random.sample(string.ascii_letters,4))
random_name = 'Messy' + random_str + '_' + now_time_s

class MUL(models.Model):
    messyId = models.PositiveIntegerField(verbose_name='Messy号')
    is_messy = models.BooleanField(default='0',verbose_name='是否为管理员')
    name = models.CharField(max_length=100,default=random_name,verbose_name='用户名')
    email = models.EmailField(max_length=100,verbose_name='邮箱')
    passwd = models.CharField(max_length=100,verbose_name='密码')
    date_joined = models.CharField(max_length=100,default=now_time,verbose_name='注册时间')
    last_login = models.CharField(max_length=100,default='该用户注册后还没登录过',verbose_name='最后一次登录时间')
    last_login_IP = models.CharField(max_length=100,default='该用户注册后还没登录过',verbose_name='最后一次登录IP')

    class Meta:
        ordering = ['date_joined']
        verbose_name = '用户'