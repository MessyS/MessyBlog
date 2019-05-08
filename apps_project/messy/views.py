# 系统库
import requests
import hashlib
import time, random
import os, re, shutil, json, psutil, datetime, threading
from bs4 import BeautifulSoup
from itertools import chain
# django库
from django.shortcuts import render_to_response, HttpResponse, render, HttpResponseRedirect, reverse
from django.http import JsonResponse
from django.core.paginator import *
from django.db.models import Q
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
# 主项目库
from messys.settings import DEFAULT_FROM_EMAIL
# 自定义库
from apps_project.server.views import *
from apps_project.articles.models import *
from apps_project.manager.models import *
from .models import *


class Messy():
    '''一些杂项的展示页面与独立小功能'''

    @ensure_csrf_cookie
    def index(self):
        category = self.GET.get('category')
        pageId = self.GET.get('pageId')
        year = self.GET.get('year')
        month = self.GET.get('month')

        # 默认配置
        listAll = Article.objects.order_by('-time')  # 文章数查询

        if (category == None) and (pageId is None) and (year is None) and (month is None):
            pass
        elif (category == '') or (pageId == '') or (year == '') or (month == ''):
            # 若发送空数据直接返回404
            return render_to_response('404.html')
        else:
            ''' ***********************    以下为聚合查询配置逻辑（按可能性从小到大排列）    ************************ '''
            # 全部条件存在
            if (not (category is None)) and (not (year is None)) and (not (month is None)):
                start_date = datetime.date(int(year), int(month), 1)
                end_date = datetime.date(int(year), int(month), 30)
                listAll = Article.objects.order_by('-time') \
                    .filter(Q(category1__name__icontains=category) | Q(category2__name__icontains=category)) \
                    .filter(time__range=(start_date, end_date))
            # 分类、年份存在
            elif (not (category is None)) and (not (year is None)):
                listAll = Article.objects.order_by('-time') \
                    .filter(Q(category1__name__icontains=category) | Q(category2__name__icontains=category)) \
                    .filter(time__year=year)
            # 分类、月份存在
            elif (not (category is None)) and (not (month is None)):
                nowYear = time.strftime('%Y', time.localtime(time.time()))
                start_date = datetime.date(int(nowYear), int(month), 1)
                end_date = datetime.date(int(nowYear), int(month), 30)
                listAll = Article.objects.order_by('-time') \
                    .filter(Q(category1__name__icontains=category) | Q(category2__name__icontains=category)) \
                    .filter(time__range=(start_date, end_date))
            # 年份、月份存在
            elif (not (year is None)) and (not (month is None)):
                start_date = datetime.date(int(year), int(month), 1)
                end_date = datetime.date(int(year), int(month), 30)
                listAll = Article.objects.filter(time__range=(start_date, end_date))
            # 单个条件存在
            else:
                if not (category is None):
                    listAll = Article.objects.order_by('-time').filter(
                        Q(category1__name__icontains=category) | Q(category2__name__icontains=category))
                if not (year is None):
                    listAll = Article.objects.filter(time__year=year)
                if not (month is None):
                    nowYear = time.strftime('%Y', time.localtime(time.time()))
                    start_date = datetime.date(int(nowYear), int(month), 1)
                    end_date = datetime.date(int(nowYear), int(month), 30)
                    listAll = Article.objects.filter(time__range=(start_date, end_date))
                    
        ''' **************************************    以下为分页配置    ******************************************* '''
        paginator = Paginator(listAll, 10)  # 分页器配置
        if not (pageId is None):
            articlesList = paginator.page(pageId)
        else:
            articlesList = paginator.page(1)

        ''' **************************************    以下为数据返回    ****************************************** '''
        # 热门文章
        hotList = Article.objects.order_by('-traffic')[:3]
        # 随机推荐
        randomList = Article.objects.order_by('?')[:6]
        # 智能推荐（算法优化中，暂时用随机推荐代替）
        likeList = Article.objects.order_by('?')[:6]

        # 所有分类(排除第一个:New)
        categoryList = Category.objects.exclude(id__exact=1)

        # 历史归档
        archive = Article.objects.dates('time', 'month', order='DESC')

        # 必应图
        bgiApi = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&pid=hp'
        q = requests.get(bgiApi)
        endUrl = q.json()['images'][0]['url']
        bgiAllUrl = 'https://cn.bing.com/%s&w=950&h=535' % endUrl

        data = {
            # 文章分页器分页数据
            'articlesList': articlesList,
            # 必应每日一图
            'bgiAllUrl': bgiAllUrl,

            # 侧边栏功能
            'hotList':hotList,
            'randomList': randomList,
            'likeList': likeList,
            'categoryList': categoryList,
            'archive': archive,

            # 分页器
            'pagesList': paginator.page_range,
        }

        return render_to_response('index.html', data)

    def randomPhotos(self):
        data = photos.objects.order_by('?')[:4]
        list = []
        for i in data:
            list.append(i.imgS)
        return JsonResponse(list,safe=False)

    @ensure_csrf_cookie
    def photos(self):
        Access().UserInfo(self)
        return render_to_response('photos.html')

    def photosAjax(self):
        if self.method == 'POST':
            nums = self.POST.get('n')
            month = self.POST.get('m')

            if (nums is None) and (month is None):
                data = photos.objects.order_by('-time')[:30]
            elif not(nums is None) and not(month is None):
                nowYear = time.strftime('%Y', time.localtime(time.time()))
                start_date = datetime.date(int(nowYear), int(month), 1)
                end_date = datetime.date(int(nowYear), int(month), 30)
                data = photos.objects.filter(time__range=(start_date, end_date))[:int(nums)]
            elif not(nums is None):
                data = photos.objects.order_by('-time')[:int(nums)]
            elif not(time is None):
                nowYear = time.strftime('%Y', time.localtime(time.time()))
                start_date = datetime.date(int(nowYear), int(month), 1)
                end_date = datetime.date(int(nowYear), int(month), 30)
                data = Article.objects.filter(time__range=(start_date, end_date))

            listData = []
            for i in data:
                listData.append({
                    'id':i.id,
                    'author': i.author.name,
                    'time': i.time,
                    'describe': i.describe,
                    'imgS':i.imgS,
                    'imgB':i.imgB,
                })

            listDataAll = {
                'listAllNums':len(photos.objects.all()),
                'listData':listData,
            }

            return JsonResponse(listDataAll)
        else:
            return render_to_response('404.html')

    def rockcloud(self):
        Access().UserInfo(self)

        serKey = self.GET.get('serKey')
        page = self.GET.get('page')
        if serKey == 'Messy':
            return render_to_response('rockcloud/' + page + '.html')
        else:
            return render_to_response('404.html')

    # 赞赏页
    @ensure_csrf_cookie
    def goodBoy(self):
        Access().UserInfo(self)

        # 排名获取
        rankingList = goodBoyList.objects.order_by('-money')
        rankingThree = []
        rankingThreeNum = []
        for i in range(3):
            num = rankingList[i].id
            rankingThreeNum.append(rankingList[i].id)
            rankingThree.append(goodBoyList.objects.get(id=num))

        # 剩下的数据数据排列
        listRandom = []
        list = goodBoyList.objects.exclude(id=rankingThreeNum[0]) \
            .exclude(id=rankingThreeNum[1]) \
            .exclude(id=rankingThreeNum[2])
        for i in list:
            listRandom.append(i)
        random.shuffle(listRandom)

        # 总个数
        totalNum = len(rankingList)

        return render_to_response('goodBoy.html', {
            'ranking': rankingThree,  # 前三数据
            'totalNum': totalNum,  # 总个数
            'list': listRandom,  # 随机排列名单
        })

    # 个人详情页
    @ensure_csrf_cookie
    def about(self):
        Access().UserInfo(self)
        return render_to_response('about.html')

class MessyFun:
    def test(self):
        # data = Article.objects.all()
        #
        # for i in data:
        #     front_context = re.sub('link','', i.front_context)
        #     front_context = re.sub('script','',front_context)
        #     i.front_context = front_context
        #     i.save()
        #     print('【%s】处理完成' % i.name)
        return render_to_response('test.html')

    def siteSearchHot(self):
        '''热词数据回显'''
        searchDataHotList = []
        list = searchHistory.objects.order_by('-count')[:15]
        for i in list:
            searchDataHotList.append(i.keyword)
        return JsonResponse(searchDataHotList, safe=False)

    def siteSearch(self):
        '''关键词搜索'''
        Access().UserInfo(self)
        if self.method == 'POST':
            keyword = str(self.POST.get('keyword'))

            # 搜索关键词数据库增加
            keywordSearched = searchHistory.objects.filter(keyword__iexact=keyword)
            if keywordSearched.exists():
                searchCount = keywordSearched[0]
                searchCount.count += 1
            else:
                searchCount = searchHistory(keyword=keyword, count=1)
            searchCount.save()

            # 总数据存储数组
            searchDataJson = []

            # 一级数据查询（按标题）
            searchDataOne = Article.objects.order_by('-time').filter(name__icontains=keyword)
            for i in searchDataOne:
                json = {
                    'id': i.id,
                    'title': i.name,
                    'filter': 'title',
                }
                searchDataJson.append(json)

            # 二级数据查询（按文章内容）
            searchDataTwo = Article.objects.order_by('-time').filter(front_context__icontains=keyword)

            # 数据去重
            searchDataId = []  # 一级查询id存储
            for i in searchDataOne:
                searchDataId.append(i.id)
            for i in searchDataTwo:
                if i.id in searchDataId:
                    pass
                else:
                    json = {
                        'id': i.id,
                        'title': i.name,
                        'filter': 'content',
                    }
                    searchDataJson.append(json)

            return JsonResponse(searchDataJson, safe=False)
        else:
            return render_to_response('404.html')