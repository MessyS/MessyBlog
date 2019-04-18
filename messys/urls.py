"""messys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render_to_response

def biZhan(req):
    return render_to_response('test.html')

urlpatterns = [
    # path('admin/', admin.site.urls),
    #  path('',biZhan),

    path('',include('apps_project.messy.urls')),
    path('',include('apps_project.manager.urls')),
    path('',include('apps_project.server.urls')),
    path('',include('apps_project.articles.urls')),
    path('',include('apps_project.oauth.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)