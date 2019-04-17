from django.urls import path
from . import views

urlpatterns = [
    # 管理主台
    path('manager/',views.Manager.index, name='manager'),

    # 系统操作
    path('reboot/',views.Server.reboot,name='reboot'),

    # 邮件发送
    path('emailSend/',views.Email.emailSend, name='emailSend'),
    path('emailTest/',views.Email.emailTest, name='emailTest'),

    # 文章管理
    path('addHF_article/',views.Articles.addHF, name='addArticlesApp'),
    path('addHFHtml_article/',views.Articles.addHFHtml, name='addArticlesHtml'),
    path('del_article/',views.Articles.delMeg, name='delArticles'),

    # 鸣谢列表
    path('listShowJson/',views.GoodBoy.listShowJson, name='GoodBoyJson'),
    path('addGoodBoyMeg/',views.GoodBoy.addMeg, name='addGoodBoyMeg'),
    path('alterGoodBoyMeg/',views.GoodBoy.alertMeg, name='alertGoodBoyMeg'),
    path('delGoodBoyMeg/',views.GoodBoy.delMeg, name='delGoodBoyMeg'),
]