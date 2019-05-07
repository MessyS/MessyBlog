from django.urls import path
from . import views

urlpatterns = [
    path('',views.Messy.index, name='index'),
    path('randomPhotos/',views.Messy.randomPhotos, name='randomPhotos'),

    # 摄影图展示
    path('photos/',views.Messy.photos, name='photos'),
    path('photosAjax/',views.Messy.photosAjax, name='photosAjax'),
    # 关于我展示
    path('about/',views.Messy.about,name='about'),
    # 赞赏页展示
    path('goodBoy/',views.Messy.goodBoy,name='goodBoy'),

    # 全文索引
    path('siteSearch/',views.MessyFun.siteSearch,name='siteSearch'),
    # 热词展示
    path('siteSearchHot/',views.MessyFun.siteSearchHot,name='siteSearchHot'),

    # 测试
    path('test/',views.MessyFun.test, name='test'),

    # 磐云
    path('rockcloud/',views.Messy.rockcloud, name='rockcloud'),
]