# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#pylint: disable=import-error
import sys
import os
sys.path.append("../")
import wechat
import json
import time
import datetime
from mytimer import get_time_distanse
from wechat import WeChatManager, MessageType
from Imgdecode import decodeing
from sqliteop import insert_db , select_db
from pic_search import search_pic
import threading
from PIL import Image
import config
import re
from redwhite import get_redwhite_pic
from selector import Selector
personal_id="wxid_pkfm888mt7zd22"
wechat_manager = WeChatManager(libs_path='./libs')
sqlite_url="../Web/db.sqlite3"
imgstore_url="../Web/media/img"
chatroom='24803859571@chatroom'
pic_search_flag=0
# 这里测试函数回调
@wechat.CONNECT_CALLBACK(in_class=False)
def on_connect(client_id):
    print('[on_connect] client_id: {0}'.format(client_id))

@wechat.RECV_CALLBACK(in_class=False)
def on_recv(client_id, message_type, message_data):
    print('[on_recv] client_id: {0}, message_type: {1}, message:{2}'.format(client_id,
                                                                            message_type, json.dumps(message_data,ensure_ascii=False)))


@wechat.CLOSE_CALLBACK(in_class=False)
def on_close(client_id):
    print('[on_close] client_id: {0}'.format(client_id))


# 这里测试类回调， 函数回调与类回调可以混合使用
class LoginTipBot(wechat.CallbackHandler):
    def __init__(self):
        self.select_obj=None

    # @wechat.CONNECT_CALLBACK(in_class=True)
    # def on_connect(self, client_id):


    @wechat.RECV_CALLBACK(in_class=True)
    def on_message(self, client_id, message_type, message_data):
        global pic_search_flag
        def startTimer(): 
            
            if timer != None: 
                data=select_db(datetime.datetime.now(),sqlite_url) 
                wechat_manager.send_text(client_id,'wxid_pkfm888mt7zd22','预定时间已到')
                string="今天的图片发送情况:\n昨日22时至今日22时总共发送了{}张图片\n".format(data[0])
                for key in data[1]:
                    temp="{}\t\t:{}\n".format(key,data[1][key])
                    string+=temp
                string+="望各位群友再接再厉"
                wechat_manager.send_text(client_id,"24803859571@chatroom",string)
                #timer.finished.wait(get_time_distanse(datetime.datetime.now(),config.time_setting))
                time.sleep(1)
                timer.finished.wait(get_time_distanse(datetime.datetime.now(),config.time_setting))
                timer.function()
        if message_type == 11025:
            self.select_obj=Selector(wechat_manager,client_id)
            timer=threading.Timer(get_time_distanse(datetime.datetime.now(),config.time_setting),startTimer)
            timer.start()
            

        if message_type == 11046:
            self.select_obj.select(message_type,message_data)
            if message_data["msg"][0]== "#":
                
                try:
                    if message_data["msg"]== "#课代表":
                        #对上了以后，开始将flag置为1，进行while等待然后开始使用pic_search中的函数,获取链接后将图片和链接发送出去
                        #当flag==1时，图片操作将改变
                        pic_search_flag=1
                        wechat_manager.send_text(client_id,personal_id,'收到收到收到收到，请发送你想要查询的图片')
                        # def waiting():
                        #     global pic_search_flag
                        #     if pic_search_flag==1:
                        #         wechat_manager.send_text(client_id,chatroom,'一分钟了,没图说个J8！')
                        #         pic_search_flag=0
                        # timer=threading.Timer(60,waiting)
                        # timer.start()
                    elif message_data["msg"][0:3]=="#红白" and len(message_data["msg"])>3:
                        match=re.search("#红白\n(.*)\n(.*)",message_data["msg"])
                        temp_url=get_redwhite_pic(match.group(1),match.group(2))
                        wechat_manager.send_image(client_id,personal_id,temp_url)
                    else:
                        raise Exception("泥嗦的是个撒子哦")
                except Exception as e:
                    pass
                    # wechat_manager.send_text(client_id,personal_id,str(e))
        if message_type == MessageType.MT_RECV_PICTURE_MSG and (message_data["room_wxid"] == chatroom  or 
            message_data["room_wxid"]=='') and message_data["from_wxid"]!="wxid_8pn6il5eyqse22":
            #这里有报错的需要修改一下啊
            imgurl=message_data["image"]
            time.sleep(1)
            pic_name,state,height,width,md5=decodeing(imgurl,message_data['xor_key'],imgstore_url)
            
            if state == 0:
                #第一层验证，图片大于100KB




                #搜图程序
                try:
                    if pic_search_flag==1:
                        #TODO:没有什么好的办法进行
                        pic_search_flag=0
                        wechat_manager.send_text(client_id,personal_id,'正在查询中...')
                        [temp_url,links]=search_pic("..\\Web\\media\\img\\"+pic_name)
                        #发送预览图和链接
                        wechat_manager.send_image(client_id,personal_id,temp_url)
                        string="经过搜索，有以下链接可能是此图来源\n"
                        for i in links:
                            string+=i+"\n"
                        string+="康一康有没有你想要的"
                        wechat_manager.send_text(client_id,personal_id,string)
                        os.remove("..\\Web\\media\\img\\"+pic_name)
                        return
                except Exception as e:
                    pass
                    # wechat_manager.send_text(client_id,personal_id,str(e))




            
                wechat_manager.send_text(client_id,'wxid_pkfm888mt7zd22','收到 请前往127.0.0.1进行查看')
                #TODO:
                #这里加重复性验证，就不用修改数据库！通过查阅数据库得到当日图片url，然后一个个对比，如果有相同的就删除掉现在的那个
                #问题1：通过pic_name得到大小信息 二：通过数据库查找得到今天日期的图片url
                # 三：去掉img/  让图片搜索对齐  四：遍历比较大小 五：如果有一样的就删掉
                insert_db(pic_name,sqlite_url,message_data['from_wxid'],height,width,md5)
            elif state == 1:
                wechat_manager.send_text(client_id,'wxid_pkfm888mt7zd22',"撤回太早或者是网络波动")
            elif state == 2:
                
                try:
                    if pic_search_flag==1:
                        #TODO:没有什么好的办法进行
                        pic_search_flag=0#
                        wechat_manager.send_text(client_id,personal_id,'正在查询中...')
                        [temp_url,links]=search_pic("..\\Web\\media\\img\\"+pic_name)
                        #发送预览图和链接
                        wechat_manager.send_image(client_id,personal_id,temp_url)
                        string="经过搜索，有以下链接可能是此图来源\n"
                        for i in links:
                            string+=i+"\n"
                        string+="康一康有没有你想要的"
                        wechat_manager.send_text(client_id,personal_id,string)
                        os.remove("..\\Web\\media\\img\\"+pic_name)
                        return
                except Exception as e:
                    wechat_manager.send_text(client_id,personal_id,str(e))


                os.remove("..\\Web\\media\\img\\"+pic_name)
                wechat_manager.send_text(client_id,'wxid_pkfm888mt7zd22',"图片大小不达标")
            elif state == 3:
                wechat_manager.send_text(client_id,'wxid_pkfm888mt7zd22',"不是正常格式的图片")



if __name__ == "__main__":
    bot = LoginTipBot()

    # 添加回调实例对象
    wechat_manager.add_callback_handler(bot)
    wechat_manager.manager_wechat(smart=True)

    # 阻塞主线程
    while True:
        time.sleep(0.5)
