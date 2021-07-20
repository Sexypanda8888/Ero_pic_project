#考虑到后期是根据转换出来的图片进行筛选的，所以我们使用图片URL
import os
def delete_file(url):
    path = url  # 文件路径
    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        #os.remove(path)  
        #os.unlink(path)
        return 1
    else:
        print('no such file:%s'%url)
        return 0
#如果不满足要求，就从数据库中删除文件，并向下传递结果防止数据库录入
def judge(imgurl):
    fsize = os.path.getsize(imgurl)
    if fsize<=100*1024:
        delete_file(imgurl)
        return False
    else:
        return True