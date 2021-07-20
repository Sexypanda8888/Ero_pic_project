#返回一个当日时间限制
#time_setting本来应该是一个22:22:00的类型，但是方便起见就变成整点了
import datetime
import re
def today_limit(date,time_setting):
    #date遵循xxxx-xx-xx
    Searchobj=re.search(r'([0-9]{4})-([0-9]{2})-([0-9]{2})',date)
    if not Searchobj:
        print("Wrong type of input")
    a=datetime.datetime(int(Searchobj.group(1)),int(Searchobj.group(2)),int(Searchobj.group(3))\
        ,time_setting,0,0)
    
    #对于一天来说，仅有可能是今天或者是昨天。
    #今天的这个时候和昨天的这个时候
    b=a+datetime.timedelta(days=-1)
    return [b,a]
