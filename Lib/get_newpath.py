import os
from  Config import config


def getNewPath(file_dir): #输入文件的目录
    list = os.listdir(file_dir) #获取当前目录下的所有文件，构成一个列表
    list.sort(key=lambda sample:os.path.getmtime(file_dir+"\\"+sample)) #按照最后修改文件的时间从小到大排序
    file_path = os.path.join(file_dir,list[-1])
    return file_path

if __name__ == '__main__':
    bb = getNewPath(config.log_dir)
    print(bb)