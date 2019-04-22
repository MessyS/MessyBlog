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
    MESSYSESSIN = meg.session.session_key
    sessionY = meg.session.exists(MESSYSESSIN)
    if sessionY:
        messyId = meg.session.get('MESSYID')
        messyEmail = meg.session.get('MESSYEMAIL')

        userFind = MUL.objects.filter(
            Q(messyId__exact=messyId) & Q(email__exact=messyEmail))
        if userFind.exists():
            if userFind[0].is_messy:
                pass
            else:
                return HttpResponse('03')   # 用户权限等级不够
        else:
            return HttpResponse('02')       # 不存在的用户
    else:
        return HttpResponse('01')           # 未注册的session

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
        return render(self, 'manager.html',{
            'cpu': self._serMeg['cpu'],
            'memory': self._serMeg['memory'][0],
            'bytes_rcvd': self._serMeg['network'][0],
            'bytes_sent': self._serMeg['network'][1],
            'countAll': self._count_nums.count,
            'countToday': self._today.count,
            'crawlerCountToday': self._today.crawlerCount,
        })

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

    # ip地址归属地
    def access(self):
        if self.method == 'POST':
            Access().UserInfo(self)
            userOauth(self)
            nums = self.POST.get('nums')
            apiUrl = 'http://ip.taobao.com/service/getIpInfo.php?ip='
            if int(nums) == 0:
                u = Userip.objects.order_by('-time').filter(ip_address=0)
            else:
                u = Userip.objects.order_by('-time').filter(ip_address=0)[:int(nums)]

            # 查询主程序函数
            def main():
                for i in u:
                    # 异常继续循环执行
                    def query():
                        r = requests.get(apiUrl + i.ip)
                        return r

                    while True:
                        r = query()
                        if r.status_code == 200:
                            q = r.json()
                            ip_address = q['data']['country'] + '-' + \
                                         q['data']['region'] + '-' + q['data']['city'] \
                                         + '-' + q['data']['isp']
                            i.ip_address = ip_address
                            i.save()
                            time.sleep(1)   # 淘宝的qps
                            break
                        else:
                            time.sleep(1)

            if int(nums) > 10 or int(nums) == 0:
                T = threading.Thread(target=main)
                T.start()
                return HttpResponse(2)
            else:
                main()
                return HttpResponse(1)
        else:
            return render_to_response('404.html')

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

class Photos:
    def addPhotos(self):
        '''添加摄影图片'''
        if self.method == 'GET':
            a = photos.objects.order_by('-time')
            return render_to_response('addPhotos.html',locals())
        elif self.method == 'POST':
            userOauth(self)

            # 获取上传数据
            imgList = self.FILES.getlist('imgF')

            # ************  处理图片路径 media/cameraPhotos/img格式/md5（Messy + 格式 + 时间）.jpg   *********
            imgSNameList = []
            imgMNameList = []
            imgBNameList = []
            def photoDeal(model,modelList,i):
                nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # 列表数据增加(i为循环的加盐字符，预防图片名重合)
                photoName =  'Messy%s%s%s' % (model,nowTime,i)
                photoName = hashlib.new('md5', photoName.encode('utf-8'))
                photoName = photoName.hexdigest()
                photoName = 'media/cameraPhotos/img%s/%s.jpg' % (model,photoName)
                modelList.append(photoName)

            for i in range(len(imgList)):
                photoDeal('S',imgSNameList,i)
                photoDeal('M',imgMNameList,i)
                photoDeal('B',imgBNameList,i)

            # **********************************   数据库存储    *****************************************
            for i in range(len(imgList)):
                data = photos(imgS='/%s' % imgSNameList[i],imgM='/%s' % imgMNameList[i],imgB='/%s' % imgBNameList[i],time=nowTime)
                data.author = MUL.objects.first()
                data.save()

            # **********************************  图片各种压缩   *****************************************
            def photoSave(img,w,h,width,model):
                if img.width > width:               # 原图尺寸小于需要改变的尺寸则不改变尺寸
                    newWidth = width
                    newHeight = round(newWidth / w * h)
                    img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
                if model == 'S':
                    img.save(imgSNameList[num], optimize=True, quality=85)
                elif model == 'M':
                    img.save(imgMNameList[num], optimize=True, quality=85)
                else:
                    pass
            num = 0
            for i in imgList:
                # 先存储原图
                with open(imgBNameList[num], 'wb') as destination:
                    for chunk in i.chunks():
                        destination.write(chunk)
                time.sleep(1)                   # 睡一秒存储,以防报错

                # 在进行各种压缩
                img = Image.open(imgBNameList[num])
                w, h = img.size                  # 原始图片的长宽
                photoSave(img,w,h,600,'S')           # 存小图
                photoSave(img,w,h,1500,'M')          # 存中图

                num += 1

            return HttpResponse('year!')
        else:
            return render_to_response('404.html')

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
