from django.urls import path
from . import views

urlpatterns = [
    # 文章展示
    path('articles/<str:category>/<int:page_id>',views.ArticleShow.articles,name='articles'),
    path('detail/<int:articles_id>',views.ArticleShow.detail,name='detail'),
]