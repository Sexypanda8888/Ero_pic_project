"""PIC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from app1.views import *# 添加
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('uploadImg/', uploadImg), # 新增
    path('register/', register),
    path('login/', login),
    path('out/',out),
    re_path('vote/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})$',votes,name="votes"),  #还是需要先判断日期合法性(不过有超链接就不需要判定了)
    re_path('showImg/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})$',showImg,name='showImg'),
    re_path("result/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})$",result,name='result'),
    path('',index),
#    path('media/img/<str:picname>',picshow),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  #这个到底是什么啊
