#目的是修改目前的数据库使得数据更新。
import sqlite3
import time
import pytz
import datetime
from PIL import Image
import hashlib
import os
#我只需要插入操作

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)  #md5算法本身就是分块的，因此可以多次更新  可以先读，最后再输出
    f.close()
    return myhash.hexdigest()


def insert_db(pic_name,sqlite_url,update_person,height,width,md5):
    conn = sqlite3.connect(sqlite_url)
    tz=pytz.timezone('Asia/Shanghai')
    date=datetime.datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    c = conn.cursor()
    url='img/'+pic_name
    c.execute("INSERT INTO app1_img (img_url,date,vote,update_person,delete_vote,height,width,md5) \
        VALUES ('%s',datetime('%s'), 0 ,'%s',0,%d,%d,'%s')"% (url,date,update_person,height,width,md5))
    conn.commit()
    conn.close()
    return 
conn = sqlite3.connect('./db.sqlite3')
c = conn.cursor()
cursor = c.execute("SELECT img_url from app1_img")
d = conn.cursor()
for row in cursor:
    print(row[0])
    path='media/'+row[0]
    if not os.path.isfile(path):
        continue
    md5=GetFileMd5(path)
    a=Image.open(path)
    width=a.width
    height=a.height
    d.execute("update app1_img set height=?,width=?,md5=? where img_url=?",(height,width,md5,row[0]))
conn.commit()
    