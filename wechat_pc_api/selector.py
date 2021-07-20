from wechat import MessageType
import threading
import re

from find_benzi import benzi


#需要一个共同的列表进行数据传输。

#selector需要建类吗？
"""
建立了类以后，在那边的函数进行创建。
类由demo程序创建，然后保存诸如线程池等信息。
"""
"""
关于内存管理，我认为应该创建多个正在进行的线程列表，并包含了判断所需的信息
最后靠是否alive来进行增减，每次在创建线程之前都要进行一遍清理遍历
"""
"""
现在决定，建立一个包含全部线程的表，然后同时进行@和#两套命令系统，@是最近的，#是直接指定的。
最近的由遍历线程表可以获得，直接指定则还要检查线程内容。然后严格遵照^#.*?$的方式来建立线程
只不过会让用户多一两个操作时间而已，不需要在此太过拘泥
"""


"""
创建线程函数会不会和大列表有冲突？
"""
def uncertainlist(a,other):
    """
    这个函数是针对那些不确定长度的列表的！
    """
    if len(a)>0:
        return a[0]
    else:
        return other




class Selector:
    def __init__(self,manager,client_id):
        self.manager=manager
        self.client_id=client_id
        self.commandlist=[[]]#里面包含的是msg信息（用于检验的话应该都要包含）,对它的操作必须是串行的。
        self.comiclock=threading.Condition()
        #线程池含有线程、wx_id，chatroom,service四个部分
        self.threadpool=[]

    def create_thread(self,message_data,pool,lock):
        wx_id=message_data["from_wxid"]
        chatroom=message_data["room_wxid"]
        #通过垃圾回收机制销毁已经结束的线程
        temp=[]
        for i,j,k,l in pool:
            if i.is_alive():
                temp.append([i,j,k,l])
        print(temp)
        flag=True
        for i in range(len(temp)):
            if wx_id == temp[i][1] and chatroom == temp[i][2] and lock == temp[i][3]:
                print('进入搜查阶段')
                flag=False
                t=temp[i]
                temp.pop(i)
                temp.insert(0,t)
                self.commandlist[0]=[0,-1,message_data["wx_id"],message_data["room_wxid"]]
                t[3].acquire()
                print(self.commandlist)
                t[3].notify_all()
                t[3].release()
                break
        # for _,i,j,k in temp:
        #     if wx_id == i and chatroom == j and lock==k:
        #         flag=False
        #检查重复线程，需要wx_id,chatroom
        if flag:
            temp.insert(0,
                [
                threading.Thread(
                    target=benzi,
                    args=[self.manager,self.client_id,message_data,self.commandlist,self.comiclock]
                    ),
                wx_id,
                chatroom,
                lock
                ]
                )
            temp[0][0].start()
        return temp


    def select(self,message_type,message_data):
        #如何做到多个client来做呢？虽然现在还不需要
        #  ^#(.*)[^#]$这个挺好，要有字符而且最后一个不能是井号
        if message_type == MessageType.MT_RECV_TEXT_MSG:
            match1=re.findall("^#(.*[^#])$",message_data["msg"])    #这里就规定了只有含有固定标识的语句才能够被视为命令
            match2=re.findall("^@.+ (.+)$",message_data["msg"])
            """
            还得写是否是用另一套方式来下的指令
            """
            #说明是命令信息,将信息放入命令列表
            """
            要不要把修饰符先处理掉再放入command里面？
            """
            if match1:
                if match1[0]=="本子":
                    #搜本子接口
                    """
                    考虑1：直接在每次收到以后就进行notify，让所有线程自行检查命令是否符合要求
                        第一步检查名称，群等信息是否能对上；
                        对上后，第二步检查命令格式是否符合要求，不符合则打回或者销毁
                    就选择考虑1
                    但是，如何选择
                    第一次仅需要命令符来创建线程，后面都使用@来进行处理?
                    """
                    self.threadpool=self.create_thread(message_data,self.threadpool,self.comiclock)
                else:
                    #其他创建线程命令的位置
                    pass
                    #因为还没有将全部的内容移植进去，所以不能把没有的命令一下打死
                    #self.manager.send_text(self.client_id,message_data["room_wxid"],"没有这种服务")
            #当这个符号开头但是并没有@人的时候，下面的if会报识别不到的错
            elif match2:# and uncertainlist( message_data["at_user_list"],'')=="wxid_8pn6il5eyqse22":
                if match2[0]=='撤销':
                    self.commandlist[0]=[0,-2,message_data["from_wxid"],message_data["room_wxid"]]
                else:
                    # print("正常命令")
                    self.commandlist[0]=[match2[0],0,message_data["from_wxid"],message_data["room_wxid"]]
                    """
                    突然意识到，如果用@的话，那么该如何分辨不同的请求，让他们并发呢？
                    应该是不行的
                    或者，此处阻塞，等待所有线程判断完毕后返回信息，根据处理信息进行判断是否有错误
                    """

                #这里还有问题需要修改
                #从此开始进行notify
                #但是怎么分辨要notify哪个线程池?
                """
                下一步，是从Pool中找到最近符合的线程进行notify
                """


                    #这里是必须要改的，或许让外面处理完信息和指令再传回来？
    #比如command单单把除掉定位修饰符后的结果拿出来

                service_exist=False
                for _,j,k,l in self.threadpool:
                    if j==message_data["from_wxid"] and k==message_data["room_wxid"]:
                        l.acquire()
                        l.notify_all()
                        l.release()
                        service_exist=True
                        break
                # for i in range(len(self.threadpool)):
                #     if self.threadpool[i][1]==message_data["from_wxid"] and self.threadpool[i][2]==message_data["room_wxid"]:
                #         self.threadpool[i][3].acqure()
                #         self.threadpool[i][3].notify_all()
                #         self.threadpool[i][3].release()
                #         service_exist=False
                #         #这一段向前插入的代码似乎是没有意义的，是一种冗余
                #         #但是可能可以在以后的功能拓展中用到，比如说使用#命令调优先级，不过在那边调好像就行了
                #         temp=self.threadpool[i]
                #         self.threadpool.pop(i)
                #         self.threadpool.insert(0,temp)
                #         break
                if not service_exist:
                    self.manager.send_text(self.client_id,message_data["room_wxid"],"你还没有唤醒服务呢")

#             [on_recv] client_id: 1, message_type: 11046, message:{"at_user_list": ["wxid_8pn
# 6il5eyqse22"], "from_wxid": "wxid_pkfm888mt7zd22", "is_pc": 0, "msg": "@ロボット
# さん ", "msgid": "216622979751975213", "room_wxid": "24803859571@chatroom", "tim
# estamp": 1626416590, "to_wxid": "24803859571@chatroom", "wx_type": 1}


