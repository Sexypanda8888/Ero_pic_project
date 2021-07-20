import requests
import os
import threading
import re
from bs4 import BeautifulSoup
from pic_ops import image_join ,resize_image
import time
count=0
lock=threading.Lock()

#需要一个进程同步来解决count的问题！
class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

  
    def run(self):
        self.result = self.func(*self.args)
    
    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None



def search_pic_2(pic_url):
    global count
    """
    获取sourceurl,并且下载缩略图
    返回url以及图的url
    """
    file_url="https://yande.re/post/similar"
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
    }
    path=os.path.abspath(pic_url)
    # files={'file' : open(path, 'rb')}
    files={'file':('sss.jpg',open(path, 'rb'),'image/jpg')}#不知道PNG是怎么样得
    response=requests.post(file_url,headers=headers,files=files,allow_redirects=False)
    text=response.text
    #<span class="plid">#pl https://yande.re/post/show/791564</span>
    try:
        pattern='src="(.*?)" .*? class="preview"'  
        img_nurl="https://yande.re"+re.search(pattern,text).group(1)  
        #如果没有缩略图，就说明出错，source无
        pattern="#pl (.*?)</span>"
        next_url=re.search(pattern,text).group(1)
        #如果没有查到，就不用进入next_url并且source无
        try:
            #有图的情况
            response=requests.get(next_url,headers=headers)
            text=response.text
            pattern='target="_blank" href="(.*?)"'  
            source_url=re.search(pattern,text).group(1) 
            #如果这里出错，说明大图界面没有来源 
        except:
            source_url="None"
        if not os.path.exists('./thumb'):
            os.makedirs('thumb')
        response=requests.get(img_nurl,headers=headers)
        lock.acquire()
        img_url = "./thumb/{}.jpg".format(count)  #这里是以后的事情以后就需要别的方案来改让他们同步,还有绝对路径的问题。
        count+=1
        lock.release()

        with open(img_url,'wb') as f:
            f.write(response.content)


    except:
        source_url="None"
        if os.path.exists("./thumb/no.png"):
            img_url="./thumb/no.png" #这里也不安全，万一没有这个东西
        else:
            #如果没有no图，就？
            img_url="Have no no.jpg"

    
        
#逻辑有问题，如果第一步没有后面的那么应该直接输出没有而不是去管有没有来源。
    return [source_url,img_url]

def search_pic_1(pic_url,num):
    global count
    #应该进行一个总共的
    url="https://ascii2d.net"
    file_url="https://ascii2d.net/search/file"
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57"
    }
    path=os.path.abspath(pic_url)
    # files={'file' : open(path, 'rb')}
    files={'file':('test.jpg',open(path, 'rb'),'image/jpg')}
    response=requests.post(file_url,headers=headers,files=files,allow_redirects=False)

    result_url=response.headers["Location"].split("/")[-1]
    result_url="https://ascii2d.net/search/bovw/"+result_url
    r=requests.get(result_url)
    #然后要得到前三个图片的URL，以及来源的URL
    soup = BeautifulSoup(r.content,'lxml')
    url="https://ascii2d.net"
    pics=soup.find_all(attrs={"loading":"lazy"})
    img_url=[]
    for i in range(num):
        img_nurl=url+pics[i]["src"]      #这里单个的img_url似乎不能满足要求，需要一个新的变量img_nurl
        lock.acquire()
        filename = "./thumb/{}.jpg".format(count)
        count+=1
        lock.release()
        img_url.append(filename)
        response = requests.get(img_nurl)
        if not os.path.exists('./thumb'):
            os.makedirs('thumb')
        with open(filename,'wb') as f:
            f.write(response.content)
    pic_head = {'jpg':0xffd8, 'png':0x8950, 'gif':0x4749}
    for i in range(len(img_url)):
        dat_file = open(img_url[i], "rb") 
        dat_read = dat_file.read(2)
        dat_file.seek(0,0)
        idt= dat_read[0]
        idt=idt*16*16+ dat_read[1]
        if not (idt==pic_head["jpg"] or idt==pic_head["png"] or idt==pic_head["gif"]):
            img_url[i]="./thumb/zhale.png"
        dat_file.close()
    #获取链接  通过寻找H6标签
    temp=soup.find_all("h6", limit=num)
    source_url=[]
    for i in temp:
        source_url.append(i.a["href"])

    return [source_url,img_url]

def search_pic(pic_url):
    global count
    count=0
    suffix=pic_url[-3:]
    resize_image(pic_url,"./thumb/resized."+suffix,250)
    pic_url="./thumb/resized."+suffix
    links=[]
    img_urls=[]
    threads=[]
    t1=MyThread(search_pic_1,[pic_url,3])
    threads.append(t1)
    t2=MyThread(search_pic_2,[pic_url])  #在没有括号时会报错takes 1 positional argument but 10 were given，不知道为什么
    threads.append(t2)
    for i in threads:
        i.start()
    for i in threads:
        i.join()

    #需要把结果都集合起来
    for t in threads:
        link,img_url=t.get_result()
        if type(link)==list:
            for i in link:
                links.append(i)
            for i in img_url:
                img_urls.append(i)
        else:
            img_urls.append(img_url)
            links.append(link)
    #图片合成操作
    image_join(img_urls[0],img_urls[1], "./thumb/temp.jpg", flag='vertical')
    for i in [i for i in range(2,len(img_urls))]:
        image_join("./thumb/temp.jpg",img_urls[i],"./thumb/temp.jpg",flag='vertical')

    temp_url=os.path.abspath("./thumb/temp.jpg")
    return [temp_url,links]
if __name__=="__main__":
    time1=time.time()
    try:
        img_url,links=search_pic("./resized.jpg")
        print(img_url)
        for i in links:
            print(i)
    except Exception as e:
        print(e)    # url="https://ascii2d.net"
    time2=time.time()
    print(time2-time1)