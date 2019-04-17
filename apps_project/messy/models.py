from django.db import models
import time,random,string

#常用变量
now_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
now_time_s = time.strftime('%M%S', time.localtime(time.time()))
random_str = ''.join(random.sample(string.ascii_letters,4))
random_name = 'Messy' + random_str + '_' + now_time_s

class searchHistory(models.Model):
    count = models.IntegerField(verbose_name='搜索次数')
    keyword = models.CharField(max_length=100,verbose_name='搜索关键词')

    class Meta:
        ordering = ['-count']
        verbose_name = '搜索热词'