from django.db import models
import time,random,string

#常用变量
nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
now_time_s = time.strftime('%M%S', time.localtime(time.time()))
random_str = ''.join(random.sample(string.ascii_letters,4))
random_name = 'Messy' + random_str + '_' + now_time_s

class Userip(models.Model):
    time = models.DateTimeField(default=nowTime)  # 访问时间
    ip = models.CharField(verbose_name='IP地址',max_length=30)    #ip地址
    ip_address = models.CharField(verbose_name='IP地址归属地', max_length=200,default='0')
    count = models.IntegerField(verbose_name='访问次数',default=0) #该ip访问次数
    url = models.CharField(max_length=100) #访问url地址
    shebei_meg = models.CharField(max_length=800)   #访问设备

    class Meta:
        ordering = ['time']
        verbose_name = '访问用户信息'#访问网站的ip/次数/url_path/time/设备信息
        verbose_name_plural = verbose_name

class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name='网站访问总次数',default=0)
    crawlerCount = models.IntegerField(verbose_name='爬虫访问总次数', default=0)

    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name

class DayNumber(models.Model):
    day = models.CharField(max_length=100,default='未知错误，记录默认时间' + nowTime)
    count = models.IntegerField(verbose_name='网站访问次数',default=0)
    crawlerCount = models.IntegerField(verbose_name='爬虫访问次数',default=0)

    class Meta:
        verbose_name = '网站单日访问量统计'
        verbose_name_plural = verbose_name

class OperatingHistory(models.Model):
    time = models.DateTimeField(default=nowTime)
    user = models.CharField(max_length=100,verbose_name='默认用户')
    operating = models.CharField(max_length=500,verbose_name='默认操作')
    operatingIP = models.CharField(max_length=500,verbose_name='默认IP')

    class Meta:
        ordering = ['-time']
        verbose_name = '历史操作'
        verbose_name_plural = verbose_name

class photos(models.Model):
    imgS = models.CharField(max_length=100, verbose_name='小缩略图url')
    imgM = models.CharField(max_length=100, verbose_name='中缩略图url')
    imgB = models.CharField(max_length=100, verbose_name='原图url')
    time = models.DateTimeField(default=nowTime,verbose_name='图片上传时间')
    author = models.ForeignKey('oauth.MUL',on_delete=models.CASCADE,related_name='authorCamera',verbose_name='图片作者名')
    describe = models.CharField(max_length=1000,null=True,default='这个人很懒诶,什么都没写',verbose_name='图片描述')

    class Meta:
        ordering = ['-time']
        verbose_name = '摄影图片列表'
        verbose_name_plural = verbose_name

class goodBoyList(models.Model):
    time = models.DateTimeField(default=nowTime,verbose_name='时间')
    name = models.CharField(max_length=100,verbose_name='昵称')
    note = models.CharField(max_length=500,verbose_name='备注')
    money = models.IntegerField(verbose_name='赞赏金额')

    class Meta:
        ordering = ['-time']
        verbose_name = '赞赏列表'
        verbose_name_plural = verbose_name