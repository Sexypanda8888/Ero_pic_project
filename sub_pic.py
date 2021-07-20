import os 
from PIL import Image
import numpy as np
import time
def thumb_making(pic_path,thumb_path): 
    #缩略图为方形
    pix    = 240
    origin = Image.open(pic_path)
    height = origin.height
    width  = origin.width
    if height > width: 
        #图片比较高，需要截去高的
        cur   = (height-width)/2
        tmp   = origin.crop((0,cur,width,height-cur))
        thumb = tmp.resize(( pix , pix ))
    elif width > height: 
        cur   = (width-height)/2
        tmp   = origin.crop((cur,0,width-cur,height))
        thumb = tmp.resize(( pix , pix ))
    else: 
        thumb     = origin.resize(( pix , pix ))
        pic_name  = pic_path.split('/')[-1]
        temp_list = list(pic_name)
    temp_list.insert(-4,'_thumb')
    thumb_name = ''.join(temp_list)
    route      = thumb_path+thumb_name
    thumb.save(route)
    return route

thumb_making("./1616162138.png","./")
#TODO: 还需要在上传之后进行删除图片的操作

