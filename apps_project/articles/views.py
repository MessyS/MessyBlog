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
    # 文章选择页
    @ensure_csrf_cookie
    def articles(self,category,page_id):
        Access().UserInfo(self)
        category_name = category
        page_id = page_id

        bgiApi = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&pid=hp'
        q = requests.get(bgiApi)
        endUrl = q.json()['images'][0]['url']
        bgiAllUrl = 'https://cn.bing.com/' + endUrl

        # 无参数跳转文章首页
        if category_name is None or page_id is None:
            return HttpResponseRedirect('/articles/New/1')

        if category_name == 'New':
            listAll = Article.objects.order_by('-time')
            # 进行数据分页
            paginator = Paginator(listAll,10)
            list = paginator.page(page_id)
            data = {
                'list': list,
                'bgiAllUrl': bgiAllUrl,
            }
            return render_to_response('articles.html',data)
        else:
            # 查询分类一和分类二所包含的文章
            listAll = Article.objects.order_by('-time').filter(
                Q(category1__name=category_name) | Q(category2__name=category_name))
            if len(listAll) == 0:
                return render_to_response('404.html')
            else:
                # 进行数据分页
                try:
                    paginator = Paginator(listAll, 10)
                    list = paginator.page(page_id)
                    data = {
                        'list':list,
                        'bgiAllUrl':bgiAllUrl,
                    }
                    return render_to_response('articles.html',data)
                except:
                    return render_to_response('404.html')

    # 文章详情页
    @ensure_csrf_cookie
    def detail(self,articles_id):
        Access().UserInfo(self)
        self._detail = Article.objects.filter(id__exact=articles_id)
        if self._detail.exists():
            detail = self._detail[0]
            detail.traffic += 1
            detail.save()
            return render_to_response('articleDetail.html', locals())
        else:
            return render_to_response('404.html')