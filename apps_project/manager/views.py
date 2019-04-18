# 系统库
from io import BytesIO
from PIL import Image
import requests
import hashlib
import time
import os,re, shutil, json ,psutil,datetime,threading
from bs4 import BeautifulSoup
from urllib.parse import quote
# django库
from django.shortcuts import render_to_response, HttpResponse, render, HttpResponseRedirect, reverse
from django.core.paginator import *
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail as SendMail
# 主项目库
from messys.settings import DEFAULT_FROM_EMAIL
# 自定义库
from apps_project.server.views import *
from apps_project.articles.models import *
from apps_project.manager.models import *
from apps_project.oauth.models import *

def userOauth(meg):
    '''用户认证'''
    username = meg.COOKIES.get('username', '')
    if username == 'Messy' or username == 'messygao@qq.com':
        pass
    else:
        return HttpResponse('请先登录！')

class Manager:
    def index(self):
        '''管理台主页'''
        Access().UserInfo(self)

        userOauth(self)
        self._serMeg = ServerHardware().main()
        self._count_nums = VisitNumber.objects.get(id=1)
        self._date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self._today = DayNumber.objects.get(day=self._date)
        # 返回服务器资源概览信息
        dict  = {
            'cpu':self._serMeg['cpu'],
            'memory':self._serMeg['memory'][0],
            'bytes_rcvd':self._serMeg['network'][0],
            'bytes_sent':self._serMeg['network'][1],
            'countAll':self._count_nums.count,
            'countToday':self._today.count,
            'crawlerCountToday':self._today.crawlerCount,
        }
        return render(self, 'manager.html',{'dict':dict})

class Server:
    def reboot(self):
        Access().UserInfo(self)
        if self.method == 'GET':
            return render_to_response('404.html')
        elif self.method == 'POST':
            Access().UserInfo(self)
            username = self.COOKIES.get('username')
            if username == 'Messy' or username == 'messygao@qq.com':
                def rebootChild():
                    time.sleep(300)
                    os.system('reboot')

                T = threading.Thread(target=rebootChild)
                T.start()
                return HttpResponse('系统将于5分钟后重启')
        else:
            return HttpResponse('请使用正确的方式访问本页面哟~~~')

class Email:
    def emailSend(self):
        '''邮箱'''
        if self.method == 'POST':
            if userOauth(self):
                self._title = self.POST.get('title')
                self._context = self.POST.get('context')
                self._toEmail = self.POST.get('toEmail')

                self._email_title = str(self._title)
                self._html_context = str(self._context)
                self._email_to = str(self._toEmail)
                SendMail(
                    subject=self._email_title,
                    message='',         # 只发送html文本
                    html_message=self._html_context,
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[self._email_to]
                )
                return HttpResponse('发往【' + self._email_to + '】的验证邮件已发送!请注意查收')
            else:
                return render_to_response('404.html')
        else:
            return render_to_response('404.html')

    def emailTest(self):
        return render_to_response('email.html')

class Articles:
    def addHF(self):
        '''导入md(app端)'''
        if self.method == 'POST':
            userOauth(self)
            today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # 获取ajax发来的表单信息
            category_list = self.POST.getlist('categoryList')   # 分类1/2
            fileTitleH = self.POST.get('fileTitleH')            # 文章标题
            fileContextH = self.POST.get('fileContextH')        # 文章内容
            files = self.FILES.getlist('imgF')                  # 附属图片
            x = self.POST.get('x')                         # 附属图片（宽）
            y = self.POST.get('y')                         # 附属图片（高）

            # 信息初始化
            name = fileTitleH                                   # 文章名为文件名

            category2 = ''                                      # 多标签获取与判断
            if len(category_list) == 1:
                category1 = category_list[0]
            else:
                category1 = category_list[0]
                category2 = category_list[1]

            addHF = Article(name=name, time=today_time,category1_id=category1, category2_id=category2)
            addHF.author = MUL.objects.first()

            if len(files) != 0:
                # 全局替换文章的内的图片存储地址(quote路径编码，防解析错误)
                context = re.sub(fileTitleH + '_files','/media/articlePhotos/%s' % quote(fileTitleH),fileContextH)
                addHF.context = context

                def savePhotos():                                   # 附属图片的存储
                    for f in files:                                 # 通过图片名进行去重操作
                        file_exist = os.path.exists('media/articlePhotos/' + fileTitleH + '/' + f.name)
                        if file_exist:
                            pass
                        else:
                            with open('media/articlePhotos/' + fileTitleH + '/' + f.name,'wb+') as destination:
                                for chunk in f.chunks():
                                    destination.write(chunk)
                if not files:                                       # 文件夹存在判断，防止系统错误
                    pass
                else:
                    dir_exist = os.path.exists(r'media/articlePhotos/' + fileTitleH)
                    if dir_exist:
                        savePhotos()
                    else:
                        os.mkdir(r'media/articlePhotos/' + fileTitleH)
                        savePhotos()

                # 判断首图用bgi还是img
                start = context.find('/media/articlePhotos/')
                end = context[start:].find('"') + start
                imgPath = context[start:end]

                if (int(x) > 600) or (int(y) > 300):
                    photo = "<div class='g-body-branch-photo-bgi' style='background: url(%s)'></div>" % imgPath
                else:
                    photo = "<img class='g-body-branch-photo-img' src='%s'>" % imgPath

                addHF.photo = photo
            else:
                context = fileContextH
                addHF.context = context

            # 前端展示内容（纯文本）
            top = fileTitleH
            text = BeautifulSoup(context,features="lxml").get_text()
            top_index = text.find(top)
            top_index = int(top_index) + len(top)
            del_top = text[:top_index]
            result = text.replace(del_top, '')
            front_context = result[:500]
            addHF.front_context = front_context

            # 存进数据库
            addHF.save()

            return HttpResponse('suc')
        else:
            return render(self, '404.html')

    def addHFHtml(self):
        '''导入md(网页端)'''
        if self.method == 'POST':
            userOauth(self)
            today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # 获取ajax发来的表单信息
            category_list = self.POST.getlist('categoryList')       # 分类1/2
            fileTitleH = self.POST.get('fileTitleH')                # 文章标题
            fileContextH = self.POST.get('fileContextH')            # 文章内容

            # 信息初始化
            name = fileTitleH                                   # 文章名为文件名

            category2 = ''                                      # 多标签获取与判断
            if len(category_list) == 1:
                category1 = category_list[0]
            else:
                category1 = category_list[0]
                category2 = category_list[1]

            # 创建一部分字段并存储
            addHF = Article(name=name, time=today_time,category1_id=category1, category2_id=category2)
            addHF.author = MUL.objects.first()
            addHF.context = fileContextH

            # 前端展示内容（纯文本）
            text = BeautifulSoup(fileContextH,features="lxml").get_text()
            addHF.front_context = text
            # 存进数据库
            addHF.save()

            return HttpResponse('suc')
        else:
            return render(self, '404.html')

    def delMeg(self):
        '''删除文章'''
        if self.method == 'POST':
            userOauth(self)
            article_id = self.POST.get('article_id')
            meg = Article.objects.get(id__exact=article_id)
            meg.delete()

            # 级联删除图片附件
            shutil.rmtree('media/articlePhotos/' + meg.name)
            return HttpResponse('suc')
        else:
            return render(self, '404.html')

class GoodBoy:
    def listShowJson(self):
        if self.method == 'POST':
            userOauth(self)
            '''鸣谢人员列表数据回显'''
            jsonDou = goodBoyList.objects.order_by('id')
            result = []
            for i in jsonDou:
                # 金额格式化
                money = str(round(i.money / 100,2))
                moneyIndex = money.find('.')
                moneyLen = len(money[moneyIndex:])
                if moneyLen == 2:
                    money = money + '0'

                jsonData = {
                    'id':i.id,
                    'name':i.name,
                    'note':i.note,
                    'money':money,
                }
                result.append(jsonData)
            return JsonResponse(result,safe=False)
        else:
            return render(self, '404.html')

    def addMeg(self):
        '''添加鸣谢人员'''
        if self.method == 'POST':
            userOauth(self)
            name = self.POST.get('name')
            note = self.POST.get('note')
            money = self.POST.get('money')

            if name != '' or money != '':
                list = goodBoyList(name=name,note=note,money=money)
                list.save()
                return HttpResponse('%s已加入鸣谢列表' % name)
            else:
                render_to_response('404.html')
        else:
            return render(self, '404.html')

    def alertMeg(self):
        '''修改鸣谢人员信息'''
        if self.method == 'POST':
            userOauth(self)
            id = self.POST.get('id')
            name = self.POST.get('name')
            note = self.POST.get('note')
            money = self.POST.get('money')

            if id != '' or name != '' or money != '':
                userData = goodBoyList.objects.get(id=id)
                oldName = userData.name
                userData.name = name
                userData.note = note
                userData.money = money
                userData.save()
                return HttpResponse('%s信息修改成功' % oldName)
            else:
                return HttpResponse('请填写完所有信息！')
        else:
            return render(self, '404.html')

    def delMeg(self):
        '''删除鸣谢人员信息'''
        if self.method == 'POST':
            userOauth(self)
            id = self.POST.get('id')

            if id != '':
                userData = goodBoyList.objects.get(id=id)
                name = userData.name
                userData.delete()
                return HttpResponse('%s信息删除成功' % name)
            else:
                return HttpResponse('错误！Id获取失败')
        else:
            return render(self, '404.html')
