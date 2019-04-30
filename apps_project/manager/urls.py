from django.urls import path
from . import views

urlpatterns = [
    # 管理主台
    path('manager/',views.Manager.index, name='manager'),

    # 系统操作
    path('ip_address/',views.Server.access,name='access'),
    path('reboot/',views.Server.reboot,name='reboot'),

    # 邮件发送
    path('emailSend/',views.Email.emailSend, name='emailSend'),
    path('emailTest/',views.Email.emailTest, name='emailTest'),

    # 文章管理
    path('addHF_article/',views.Articles.addHF, name='addArticlesApp'),
    path('addHFHtml_article/',views.Articles.addHFHtml, name='addArticlesHtml'),
    path('del_article/',views.Articles.delMeg, name='delArticles'),

    # 摄影图片管理
    path('addPhotos/',views.Photos.addPhotos, name='addPhotos'),
    path('delPhotos/',views.Photos.delPhotos, name='delPhotos'),
    path('desPhotos/',views.Photos.desPhotos, name='desPhotos'),
    path('desPhotosSearch/',views.Photos.desPhotosSearch, name='desPhotosSearch'),

    # 鸣谢列表
    path('listShowJson/',views.GoodBoy.listShowJson, name='GoodBoyJson'),
    path('addGoodBoyMeg/',views.GoodBoy.addMeg, name='addGoodBoyMeg'),
    path('alterGoodBoyMeg/',views.GoodBoy.alertMeg, name='alertGoodBoyMeg'),
    path('delGoodBoyMeg/',views.GoodBoy.delMeg, name='delGoodBoyMeg'),
]