from django.urls import path
from . import views

urlpatterns = [
    # 检查/登录/注册/重置
    path('auth/',views.Login.auth, name='auth'),
    path('login/',views.Login.logIn, name='login'),
    path('logout/',views.Login.logOut, name='logout'),
    path('reset/',views.Login.reset, name='reset'),
    path('signUp/',views.Login.signUp, name='signUp'),
]