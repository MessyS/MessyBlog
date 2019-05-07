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
from django.views.decorators.csrf import ensure_csrf_cookie
# 主项目库
from messys.settings import DEFAULT_FROM_EMAIL
# 自定义库
from apps_project.server.views import *
from apps_project.articles.models import *

class ArticleShow:
    # 文章详情页
    @ensure_csrf_cookie
    def detail(self,articles_id):

        # 访问记录与文章访问量
        Access().UserInfo(self)

        self._detail = Article.objects.filter(id__exact=articles_id)
        if self._detail.exists():
            detail = self._detail[0]
            detail.traffic += 1
            detail.save()

        ''' ****************************************** 侧边栏功能返回 *********************************************  '''
        # 随机推荐
        randomList = Article.objects.order_by('?')[:6]

        # 智能推荐（算法优化中，暂时用随机推荐代替）
        likeList = Article.objects.order_by('?')[:6]

        # 所有分类(排除第一个:New)
        categoryList = Category.objects.exclude(id__exact=1)

        # 历史归档
        archive = Article.objects.dates('time', 'month', order='DESC')

        # 获取文章数据
        articleData = Article.objects.get(id__exact=articles_id)

        data = {
            'detail':articleData,
            # 侧边栏功能
            'randomList':randomList,
            'likeList':likeList,
            'categoryList':categoryList,
            'archive':archive,
        }

        return render_to_response('articleDetail.html', data)