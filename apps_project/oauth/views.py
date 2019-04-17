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
from apps_project.oauth.models import *
from apps_project.oauth.models import *
from apps_project.messy.views import *
from apps_project.server.views import *

class Login:
    # 登出（删除cookie）
    def logOut(self):
        response = HttpResponseRedirect('/')
        response.delete_cookie('username')
        return response

    # 登录
    def logIn(self):
        if self.method == 'POST':
            Access().UserInfo(self)
            # 获取表单信息
            user = self.POST.get('user')
            passwd = self.POST.get('pwd')

            # 判断是否需要查询的条件
            try:
                user = int(user)
                userData = MUL.objects.all().filter(Q(messyId__exact=user) | Q(email__exact=user))
            except:
                userData = MUL.objects.all().filter(email__exact=user)
            if len(userData) == 0:
                # 没有该用户
                return HttpResponse('err')

            # 验证是否有条件相符的用户
            for i in userData:
                join_time = i.date_joined
                passwd = messyFun().md5_salt(passwd, join_time)

                if passwd == i.passwd:
                    # 全部信息正确记录最后一次登录时间和IP
                    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    # ip地址
                    if 'HTTP_X_FORWARDED_FOR' in self.META:  # 获取ip
                        client_ip = self.META['HTTP_X_FORWARDED_FOR']
                        client_ip = client_ip.split(",")[0]
                    else:
                        client_ip = self.META['REMOTE_ADDR']
                    i.last_login_IP = client_ip
                    i.last_login = now_time
                    i.save()

                    # 返回相应的数据
                    response = HttpResponse('userSuc')
                    if i.is_messy == 1:
                        response = HttpResponse('adminSuc')

                    response.set_cookie('username', i.name,10800)  # 一天cookie有效期
                    return response
                else:
                    return HttpResponse('err')
        else:
            return render_to_response('404.html')

    # 重置密码
    def reset(self):
        if self.method == 'POST':
            Access().UserInfo(self)
            # 获取表单信息
            email = self.POST.get('email')
            oldPwd = self.POST.get('oldPwd')
            newPwd = self.POST.get('newPwd')

            if email != '' and oldPwd != '' and newPwd != '':
                emailExists = MUL.objects.filter(email__exact=email)
                if emailExists.exists():
                    userData = MUL.objects.get(email__exact=email)
                    oldPwd = messyFun().md5_salt(oldPwd, userData.date_joined)
                    if oldPwd == userData.passwd:
                        userData.passwd = messyFun().md5_salt(newPwd, userData.date_joined)
                        userData.save()
                        return HttpResponse('suc')
                    else:
                        # 密码错误
                        return HttpResponse('err2')
                else:
                    # 没有该用户
                    return HttpResponse('err2')
        else:
            return render_to_response('404.html')

    # 注册
    def signUp(self):
        if self.method == 'POST':
            Access().UserInfo(self)
            email = self.POST.get('email')
            passwd = self.POST.get('pwd')

            # 判断为空
            if email != '' and passwd != '':
                emailExists = MUL.objects.filter(email__exact=email)
                if emailExists.exists():
                    # 邮箱被注册过
                    return HttpResponse('err2')
                else:
                    # 随机不重合id号
                    while True:
                        MessyId = round(random.random() * 1e9)
                        MessyIdExists = MUL.objects.filter(messyId__exact=MessyId)
                        if MessyIdExists.exists():
                            MessyId = round(random.random() * 1e9)
                        else:
                            break

                    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    passwd = messyFun().md5_salt(passwd, now_time)

                    # ip地址
                    if 'HTTP_X_FORWARDED_FOR' in self.META:  # 获取ip
                        client_ip = self.META['HTTP_X_FORWARDED_FOR']
                        client_ip = client_ip.split(",")[0]
                    else:
                        client_ip = self.META['REMOTE_ADDR']

                    addUser = MUL(messyId=MessyId,email=email, passwd=passwd,date_joined=now_time,last_login_IP=client_ip)

                    addUser.save()
                    return HttpResponse('suc')
            else:
                # 值没正确填写完
                return HttpResponse('err1')
        else:
            return render_to_response('404.html')