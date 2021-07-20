from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Img(models.Model):
    img_url = models.ImageField(upload_to='img') # upload_to指定图片上传的途径，如果不存在则自动创建
    date=models.DateTimeField(null=True)
    vote=models.IntegerField(default=0)
    update_person=models.CharField(max_length=50)
    delete_vote=models.IntegerField(default=0)
    width=models.IntegerField(null=True)
    height=models.IntegerField(null=True)
    md5=models.CharField(null=True,max_length=33)
class user_1(models.Model):
    userid=models.CharField(max_length=50 ,primary_key=True)  #和user是一对一的关系  
    wx_id=models.CharField(max_length=50,default='')
    mvp_time=models.IntegerField(default=0)
    points=models.IntegerField(default=0)
    last_vote_date=models.DateField(null=True) #用于记录
    last_delete_vote_date=models.DateField(null=True)
class wx_ids(models.Model):
    wx_id=models.CharField(max_length=20 ,primary_key=True)
    used=models.BooleanField(default=False)
#接下来需要把auth_user的表输进来