# 系统库
import requests
import hashlib
import time
import os,re, shutil, json ,psutil,datetime,threading
from bs4 import BeautifulSoup
# django库
from django.shortcuts import render_to_response, HttpResponse, render, HttpResponseRedirect, reverse
from django.core.paginator import *
from django.db.models import Q
from django.core.mail import send_mail
# 主项目库
from messys.settings import DEFAULT_FROM_EMAIL
# 自定义库
from apps_project.manager.models import *
from apps_project.oauth.models import *

class ServerHardware:
    '''服务器资源监视'''
    def __init__(self):
        self.__now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.__serverStartTime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    def cpu(self):
        self._cpuCount = psutil.cpu_count(logical=False)						# 查看cpu物理个数
        self._cpu = str(psutil.cpu_percent(interval=2, percpu=False)) + '%'		# CPU的使用率
        return self._cpu

    def memory(self):
        self._free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))
        self._total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))
        self._memory = int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total)	# 物理内存使用率(DDR)
        self._memory = str(int(self._memory * 100)) + '%'
        list = [self._memory,self._free,self._total]
        return list

    def user(self):
        self._users_count = len(psutil.users())							# 当前登录用户名
        self._users_list = ",".join([u.name for u in psutil.users()])	# 用户个数
        list = [self._users_count,self._users_list]
        return list

    def network(self):
        self._net = psutil.net_io_counters()
        self._bytes_rcvd = '{0:.2f} Mb'.format(self._net.bytes_sent / 1024 / 1024)	# 网卡接收流量
        self._bytes_sent = '{0:.2f} Mb'.format(self._net.bytes_recv / 1024 / 1024)	# 网卡发送流量
        list = [self._bytes_rcvd,self._bytes_sent]
        return list

    def main(self):
        list = {
            'now_time':self.__now_time,
            'serverStartTime':self.__serverStartTime,
            'cpu':self.cpu(),
            'memory':[
                self.memory()[0],
                self.memory()[1],
                self.memory()[2],
            ],
            'user':[
                self.user()[0],
                self.user()[1],
            ],
            'network':[
                self.network()[0],
                self.network()[1],
            ]
        }
        return list

class crawler:
    '''爬虫检测'''
    def checkIP(self, ipaddr):
        # ip格式检测
        addr = ipaddr.strip().split('.')
        if len(addr) != 4:
            return False
        for i in range(4):
            try:
                addr[i] = int(addr[i])
            except:
                return False
            if addr[i] <= 255 and addr[i] >= 0:
                pass
            else:
                return False
            i += 1
        else:
            return True

    def Ban(self, meg):
        # ip地址
        if 'HTTP_X_FORWARDED_FOR' in meg.META:  # 获取ip
            ip = meg.META['HTTP_X_FORWARDED_FOR']
            ip = ip.split(",")[0]
        else:
            ip = meg.META['REMOTE_ADDR']

        if ip != '127.0.0.1':
            userAgent = meg.environ.get("HTTP_USER_AGENT")  # 获取设备头信息
            if len(userAgent) >= 10:
                agentAllowList = ['Mozilla','Baidu']
                crawler = True
                for i in agentAllowList:
                    if userAgent.find(i) != -1:
                        crawler = False

                if crawler or self.checkIP(ip) == False:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True

class Access:
    '''访问记录'''
    def __init__(self):
        self.count_nums = VisitNumber.objects.filter(id=1)
        self.date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.today = DayNumber.objects.filter(day=self.date)
        self.now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    # 总访问数增加
    def VisitN(self):
        if self.count_nums:
            count_nums = self.count_nums[0]
            count_nums.count += 1
        else:
            count_nums = VisitNumber()
            count_nums.count = 1
        count_nums.save()

    # 当日访问时增加
    def DayN(self):
        if len(self.today) != 0:
            temp = self.today[0]
            temp.count += 1
        else:
            temp = DayNumber()
            temp.day = self.date
            temp.count = 1
        temp.save()

    # 访问用户信息记录
    def UserInfo(self, meg):
        # 总访问量与今日访问量增加
        self.VisitN()
        self.DayN()

        # ip地址
        if 'HTTP_X_FORWARDED_FOR' in meg.META:  # 获取ip
            client_ip = meg.META['HTTP_X_FORWARDED_FOR']
            client_ip = client_ip.split(",")[0]
        else:
            client_ip = meg.META['REMOTE_ADDR']

        # 访问路径
        path = meg.path
        # 访问请求头
        shebei_meg = meg.environ.get("HTTP_USER_AGENT")

        # 防止爬虫、无效ip、无效请求头加入数据库
        if crawler().Ban(meg) == 0:
            shebei_meg = '爬虫皮娃!   ' + shebei_meg

        # 判断用户信息是否访问过本站
        user_meg = Userip.objects.filter(ip=str(client_ip), url=str(path), shebei_meg=str(shebei_meg))
        list_exist = len(user_meg) > 0

        # 如果用户信息全相同，则count+=1，否新插入一条数据
        if list_exist:
            u = Userip.objects.get(ip=client_ip, url=path, shebei_meg=shebei_meg)
            u.count += 1
            u.time = self.now_time
        else:
            u = Userip()
            u.ip = client_ip
            u.url = path
            u.count = 1
            u.time = self.now_time
            u.shebei_meg = shebei_meg

        u.save()

        if crawler().Ban(meg) == 0:
            count_nums = VisitNumber.objects.get(id=1)
            date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            today = DayNumber.objects.get(day=date)
            # 爬虫总数增加
            count_nums.crawlerCount += 1
            count_nums.save()
            # 今日爬虫数增加
            today.crawlerCount += 1
            today.save()
            return False
        else:
            return True

class messyFun:
    # md5加密处理函数
    def md5_salt(self, str, salt):
        passwd = str + salt
        md5_encode = hashlib.new('md5', passwd.encode('utf-8'))
        passwd = md5_encode.hexdigest()
        return passwd

    def heavy(self, list):
        dic = {}
        ptr = 0
        while True:
            if ptr >= len(list):
                break
            if list[ptr] in dic:
                list.pop(ptr)
                ptr -= 1
            else:
                dic[list[ptr]] = 1
            ptr += 1