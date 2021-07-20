#pylint: disable-msg = import-error,unused-wildcard-import,no-member
import sys
sys.path.append('../')
import datetime
import config
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import auth
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app1.models import *






# Create your views here.


@login_required
def uploadImg(request): # 图片上传函数
    if request.method == 'POST':
        #print("the POST method")
        # concat = request.POST
        # postBody = request.body
        # print(concat)
        # print(type(postBody))
        # print(postBody)
        img_url=request.FILES.get('img')
        nickname=request.user.get_username()
        wxid=user_1.objects.get(userid=nickname)
        if img_url:
            img = Img(img_url=img_url,update_person=wxid,
                date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            img.save()
    return render(request, 'imgupload.html')

@login_required
def showImg(request,year="",month="",day=""):
    date_of_pics=year+"-"+month+"-"+day
    from app1.utility import today_limit
    a,b=today_limit(date_of_pics,config.time_setting)
    imgs = Img.objects.filter(date__range=(a,b)) # 从数据库中取出所有的图片路径
    context = {
        'imgs' : imgs
    }
    return render(request, 'showImg.html', context)

    #在搜查数据库的时候还需要进行图片是否存在的检测吗？
    #还应该有一个检查当前数据库中图片是否相同的检测（通过检测大小，完全一样则）
    #以后数据库甚至可以存放大小数据

def register(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        wxid=request.POST.get('wxid')
        pwd2=request.POST.get('pwd2')
        if pwd!=pwd2:
            return HttpResponse('两次密码输入不一致')    
        User.objects.create_user(username=name,password=pwd)    #这 为什么没有报错呀， last name啥的不是非空的吗？
        user1=user_1(userid=name,wx_id=wxid,mvp_time=0,points=0)
        user1.save()
        return  redirect('/login')
    return render(request ,'register.html')


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    username = request.POST.get("name")
    password = request.POST.get("pwd")
    user_obj = auth.authenticate(username=username, password=password)
    if not user_obj:
        return render(request, 'login.html')
    else:
        auth.login(request, user_obj)
        path = request.GET.get("next") or "/"
        return redirect("/")
    return render(request, 'login.html')
def out(request):
    auth.logout(request)
    return redirect('/login/')


#vote应该只有投票功能，所以三者不在的情况下需要转向使用showImg来进行
@login_required
def index(request):

    #给html页面一个数据库种所有日期的set，从而让它一个个来创建链接
    username = request.user.get_username()
    judgedate=datetime.datetime(1,1,1,config.time_setting,0,0)
    p=Img.objects.all()
    q=p
    datelist=[]
    #获取每个单独的日期
    #日期的计算可以靠datetime
    while q:
        p=q.values('date').first()
        #开始判断是哪一天
        print(type(p['date']))
        #m=p['date'].strftime("%Y-%m-%d %H:%M:%S").split(' ')
        m=str(p['date']).split(' ')
        m[0]=m[0].split('-')
        #[['2021','03','08'],'time']
        n=[i for i in m[0]]
        n.append(m[1])
        #如果大于等于，则说明它应该放入下一天的内容里面
        flag=datetime.datetime(1,1,1,int(n[3][:2]),0,0).__ge__(judgedate)
        datelmt=datetime.datetime(int(m[0][0]),int(m[0][1]),int(m[0][2]),config.time_setting,0,0)
        if not flag:
            datelist.append(m[0])
            date_tmp=datelmt+datetime.timedelta(days=-1)
            q=q.exclude(date__range=(date_tmp,datelmt))
        else:
            date_tmp=datelmt+datetime.timedelta(days=+1)
            datelist.append(date_tmp.strftime("%Y-%m-%d").split('-'))
            q=q.exclude(date__range=(datelmt,date_tmp))
    datelist.reverse()

    #判断今天是哪一天，应该可以继续简化成函数
    today=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datelmt1=datetime.datetime(int(today[0:4]),int(today[5:7]),int(today[8:10]),config.time_setting,0,0)
    if datelmt1.__ge__(datetime.datetime.now()):
        #是今天，昨天22到今天22
        datelmt2=datelmt1+datetime.timedelta(days=-1)
        is_today=True
        vote_date=(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    else:
        #不是今天，今天22到明天22   (本来应该是明天10点，但是目前没有好的想法)
        date_tmp=datelmt1
        daelmt1=datelmt1+datetime.timedelta(days=+1)
        datelmt2=date_tmp
        is_today=False
        vote_date=datetime.datetime.now().strftime("%Y-%m-%d")
    #这里设定了datelmt2小于datelmt1
    if Img.objects.filter(date__range=(datelmt2,datelmt1)).exists():
        display_result=1  #今天有图片，就至少从第二个开始  今天无 0  
    else:      #这应该有更简洁的写法来着
        display_result=0
    #投昨天的票，因此需要确定有没有昨天，有的话就输入日期，并且结果要是投票日期之后的
    #这部分的01逻辑不是很好，但是可以起作用
    #range为vote_date的那一天内，可以写一个函数来生成对应的范围了
    from app1.utility import today_limit
    a,b=today_limit(vote_date,config.time_setting)
    if Img.objects.filter(date__range=(a,b)).exists():
        vote_date=vote_date.split('-')
        display_result=datelist.index(vote_date)
    else:
        vote_date=None

    
    

    print(vote_date)
    content={
        'show_dates':datelist,
        'vote_date':vote_date,
        'index':display_result,
    }
    return render(request,'index.html',content)


@login_required
def votes(request,year="",month="",day=""):     #这个，日期该怎么修改呀
    m=user_1.objects.get(userid=request.user.get_username())
    date_now=datetime.datetime.now().strftime("%Y-%m-%d")
    date_of_pics=year+"-"+month+"-"+day         #预想里是今天收集今天的，明天进行今天的投票，但是日期的改动却不会了。
    if not date_of_pics==(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d"):
        return HttpResponse("该日投票已结束或未开始")
    if request.method=="POST":
        delete=request.POST.get("delete")
        lists=request.POST.getlist("box")
        if delete=='on':
            if str(m.last_delete_vote_date)==date_now:
                return HttpResponse('你今天已经投过一次删除票了')
        else:
            if str(m.last_vote_date)==date_now:
                return HttpResponse('你今天已经投过一次票了！')
        #投票操作
        for i in lists:
            p=get_object_or_404(Img,pk=i)
            if delete=='on':
                p.delete_vote+=1
            else:
                p.vote+=1
            p.save()
            #删除操作
            if p.delete_vote>=2:
                Img.objects.filter(pk=i).delete()
        #最后收尾
        if delete=='on':
            m.last_delete_vote_date=date_now
            m.save()
            return HttpResponse('投删除票成功') 
        else:
            m.last_vote_date=date_now
            m.save()
            return HttpResponse('投票成功')
    from app1.utility import today_limit
    a,b=today_limit(date_of_pics,config.time_setting)
    imgs = Img.objects.filter(date__range=(a,b))
    context = {
    'imgs' : imgs,
    'year' : year,
    'month': month,
    'day'  : day
    }
    return render(request, 'voting.html', context)
@login_required
def result(request,year="",month="",day=""):
    date_of_pics=year+"-"+month+"-"+day
    from app1.utility import today_limit
    a,b=today_limit(date_of_pics,config.time_setting)
    imgs = Img.objects.filter(date__range=(a,b)).order_by("-vote")

    context = {
    'imgs' : imgs,
    'year' : year,
    'month': month,
    'day'  : day
    }
    return render(request, 'results.html', context)


    #应该能看到所有时候的投票结果。但是当日的应该不能看到,按顺序




# def picshow(request,picname):
#     print(picname)
#     return HttpResponse('想得美')