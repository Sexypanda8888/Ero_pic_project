import threading
import time
import datetime
import sys
sys.path.append("..")
import config
#最好是每晚十点开始投票并且结束今日收图，开始下一天收图。早上八点结束投票。  这样对后端的逻辑要求大大提升了。
#那其实弄两个timer就没问题了。一个早八一个晚八
def get_time_distanse(date,time_setting,minute,second):
    #获得现在与下一个设定时间的秒数距离
    if not date:
        return 0
    date_setting = datetime.datetime.now().replace(year=date.year, month=date.month,
        day=date.day, hour=time_setting, minute=minute, second=second)
    if date.__ge__(date_setting):
        date_setting=date_setting+datetime.timedelta(days=1)
    seconds=(date_setting-date).total_seconds()
    print(seconds)
    print(date,time_setting,minute,second)
    return int(seconds)

#为什么不能在函数里面直接加timer.function(minute,second+10,count) 是错误的呢？
def startTimer(minute=51,second=0,count=0): 
    count+=1
    second=second+10
    print(count)
    timer.finished.wait(get_time_distanse(datetime.datetime.now(),14,minute,second))
    timer.function(minute,second,count)
if __name__== "__main__":
    #这个startTimer 只需要函数的名字，但是不知道如何传入参数
    # timer=threading.Timer(get_time_distanse(datetime.datetime.now(),14,51,0),startTimer)
    # timer.start()
    print(config.time_setting)