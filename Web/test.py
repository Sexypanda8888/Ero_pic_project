import datetime
import pytz
import re
# # tz=pytz.timezone('Asia/Shanghai')
# date_from=datetime.datetime(0,0,0)
# # date=datetime.datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
# date_to=datetime.datetime(0,3,8,16,0,0)
# a=Img.objects.filter(date__range=(date_from,date_to))
# print(a)

# a=datetime.datetime(1,1,1,12,23,59)
# b=datetime.datetime(1,1,1,12,24,59)
# #print(a.__gt__(b))
# print(a)
# lst="165"
# print(lst[:2])
a=re.search(r'([0-9]{4})-([0-9]{2})-([0-9]{2})','2019-14-16')
print(a.group(2))

