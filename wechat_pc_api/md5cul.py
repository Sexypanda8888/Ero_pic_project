
import hashlib
import os
import time

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
if __name__ == "__main__":
    filepath = input('请输入文件路径：')
    # 输出文件的md5值以及记录运行时间
    time_start = time.time()
    a = GetFileMd5(filepath)
    print (a,type(a))
    time_end = time.time()
    print('totally cost',time_end-time_start)