from django.db import models
from django.contrib.auth.models import User
from app1.models import user_1
#用于将user进行单次匹配的函数，但是其实应该在注册页面进行单个添加的才对
def new_user(self):
    users=User.objects.all()
    for i in users:
        if not user_1.objects.get(pk=i.usernmae):
            new=user_1(userid=i.username)
            new.save()