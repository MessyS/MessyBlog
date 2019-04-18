from django.urls import path
from . import views

urlpatterns = [
    # 文章展示
    path('detail/<int:articles_id>',views.ArticleShow.detail,name='detail'),
]