import os
import time
import judgement
import hashlib
from PIL import Image
from md5cul import GetFileMd5


pic_head = {'jpg':0xffd8, 'png':0x8950, 'gif':0x4749}  #jpg png gif
pic_tail = {'jpg':0xffd9, 'png':0x6082, 'gif':0x003B}
#该函数功能为对一张图片进行解码并放入指定文件夹,返回其名字
#state=0,正常;state=1,网络不好或者撤回过早;state=2,是图片但是没有通过检验;state=3,图片类型越界或者不是图片
def decodeing(imgurl,xor_key,store_url):
    #先判断文件是否存在，不在时等待； 之后判断文件是否下载完全；完全以后继续操作
    k=0
    state=0
    print("等待dat文件生成")
    print("第0秒",end="")
    while not os.path.exists(imgurl):
        time.sleep(1)
        print("\r", end="")
        print("第%d秒"%k,end="")
        k+=1
        if k >60:
            state=1
            return [None,1,0,0,0]
    print("\ndat文件生成!")
    time.sleep(1)
    dat_file = open(imgurl, "rb") 
    dat_read = dat_file.read(2)
    dat_file.seek(0,0)
    idt= dat_read[0]
    idt=idt*16*16+ dat_read[1]
    #如果还没加密好，就不需要解密了
    print(dat_read,idt)
    flag=1
    if idt == pic_head['jpg']:
        pic_id = '.jpg'
    elif idt == pic_head['png']:
        pic_id = '.png'
    elif idt == pic_head['gif']:
        pic_id = '.gif'
    else:
        flag=0
        #说明该文件可能是已经加密好了。
        idt= dat_read[0] ^ xor_key
        idt=idt*16*16+ dat_read[1] ^ xor_key
        if idt == pic_head['jpg']:
            pic_id = '.jpg'
        elif idt == pic_head['png']:
            pic_id = '.png'
        elif idt == pic_head['gif']:
            pic_id = '.gif'
        else :
            #不是正常文件
            state=3
            return [None,state,0,0,0]
    count = 0 
    print("等待图片下载完毕")
    print("第0秒",end="")
    while True:
        #通过重复读取
        if count >500:
            state=1
            return [None,state,0,0,0]
        dat_file.seek(-2,2)
        dat_read = dat_file.read(2)
        if flag==0:
            idt= dat_read[0] ^ xor_key
            idt=idt*16*16+ dat_read[1] ^ xor_key
        else:
            idt= dat_read[0]
            idt=idt*16*16+ dat_read[1]
        
        if idt == pic_tail['jpg']:
            break
        elif idt == pic_tail['png']:
            break
        elif idt == pic_tail['gif']:
            break
        count+=1
        print("\r", end="")
        print("第%d秒"%count,end="")
        time.sleep(1)
    print("\n图片下载完毕!")
    time_now=str(int(time.time()))
    pic_name = store_url + '/' + time_now + pic_id   #需要测试同一时间发出图片会如何应对，按照这个来改命名方式
    pic_write = open(pic_name, "wb")
    dat_file.seek(0,0)
    for dat_data in dat_file:
        for dat_byte in dat_data:
            if flag==0:
                pic_data = dat_byte ^ xor_key
                pic_write.write(bytes((pic_data,)))   #此处为什么要加括号？不明白
            else:
                pic_write.write(bytes((dat_byte,)))
    dat_file.close()
    pic_write.close()
    if not judgement.judge(pic_name):
        #图片检验函数
        state=2
        return [time_now + pic_id,state,0,0,0]
    pic=Image.open(pic_name)
    md5=GetFileMd5(pic_name)
    print("图片识别成功！")
    state=0
    return  [time_now + pic_id,state,pic.height,pic.width,md5]
#几种状态1.不是图片2.是图片但是格式不对 3.是图片但是类型不对，可以直接返回数字
#所以可以返回1.数字来表明状态 2.文件名，如果错误则为more样式
