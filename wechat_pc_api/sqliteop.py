import sqlite3
import time
import pytz
import datetime
#我只需要插入操作
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

# insert_db('dsade',"../../../Web/db.sqlite3",'panda')

#后面还需要查询操作！
def select_db(date,sqlite_url):
      """
      返回某天的图片总数、发的人及其对应数量
      返回一个字典
      """
      conn = sqlite3.connect(sqlite_url)
      date2=(date+datetime.timedelta(days=-1)).strftime("'%Y-%m-%d %H:%M:%S'")
      c = conn.cursor()
      #后面的时间可以直接沿用输入的Data，因为触发的时间就是在之前已经算好了。
      c.execute("select * from app1_img where date > {} and date< {}".format(date2,date.strftime("'%Y-%m-%d %H:%M:%S'")))
      a=c.fetchall()
      num=len(a)
      data={}
      name = set()
      #先遍历一遍把不同的名字构成字典再去++
      for i in a:
            name.add(i[4])
      for i in name:
            data[i]=0
      for i in a:
            data[i[4]]+=1
      #下一步，根据user中的名称和昵称对应关系，进行处理
      data2={}
      for key in data:
            c.execute("select * from app1_user_1 where wx_id = '{}'".format(key))
            a=c.fetchall()
            data2[a[0][6]]=data[key]
      return [num,data2]
if __name__ == "__main__":
      sqlite_url="../Web/db.sqlite3"
      date=datetime.datetime.now()
      date2=(date+datetime.timedelta(days=-1)).strftime("'%Y-%m-%d %H:%M:%S'")
      select_db(date,sqlite_url)
      #print("select * from app1_img where date > {} and date < {}".format(date2,date.strftime("'%Y-%m-%d %H:%M:%S'")))




      # sqlite_url="../Web/db.sqlite3"
      # conn = sqlite3.connect(sqlite_url)
      # tz=pytz.timezone('Asia/Shanghai')
      # date=datetime.datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
      # c = conn.cursor()
      # aa={'AlienK': 'wxid_58jmojf06okw21', 
      # 'kamikaze': 'wxid_gyv0s18lwowy22', 
      # '久遠千歲': 'wxid_o79ivn8zaw9722', 
      # 'tamanegi': 'wxid_5lv6wv4zoadb22', 
      # 'Quin': 'wxid_izp5nqgbpcee12', 
      # 'ghostrider': 'wxid_arobhikaigno12', 
      # 'Kurumi.': 'wxid_n494l7p146xe22', 
      # 'Grey to Blue': 'wxid_b5j0iul05my012', 
      # 'Echo': 'wxid_f012iteoos0a22', 
      # '君山': 'wxid_1yg15d18bv9h22', 
      # '-': 'wxid_8racbolk6alp12', 
      # '轻井泽惠': 'wxid_gtgf7o4ucpli22', 
      # '由依': 'wxid_fx8x159rgc6z21', 
      # 'cab': 'wxid_pkfm888mt7zd22', 
      # 'Left。': 'wxid_si2if762xjr522', 
      # 'FN_2100': 'wxid_nsdonbywgwnk12', 
      # '-�🐽-': 'wxid_rkf5rjn2ox0g11', 
      # 'ロボットさんん': 
      # 'wxid_8pn6il5eyqse22', 
      # 'rinrinboon': 'wxid_n76ly2xk5mtn22'}

      # for key in aa:
      #       c.execute("INSERT INTO app1_user_1 (userid,mvp_time,points,wx_id,last_delete_vote_date,last_vote_date,name_in_group)\
      #             VALUES ('%s',0, 0 ,'%s',null,null,'%s')"% (key,aa[key],key))
      # conn.commit()
      # conn.close()