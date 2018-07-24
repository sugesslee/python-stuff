#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/7/24 14:09
# @Author  : capton
# @FileName: list_file.py
# @Software: PyCharm
# @Blog    : http://ccapton.cn
# @Github  : https://github.com/ccapton
# @Email   : chenweibin1125@foxmail.com

import os,time
# 文件、文件夹寻找类 (阻塞型)
# 阻塞的设计： 为了等待调用者的耗时操作【否则很快就完成了文件的遍历任务，调用者达不到顺序操作文件(夹)的意图】
#
class FileFinder:
   def __init__(self,finderCallback):
       self.finderCallback = finderCallback
       # 文件（夹）路径下所有文件的总大小
       self.sum_size = 0
       # 调用者控制的参数，若为False,则遍历工作继续进行，若为True，则阻塞任务，等待调用者完成它的其他耗时操作后在考虑是否改变此值
       self.recycle = True
       # 调用者控制的参数，若为False,则正常工作，若为True，则当recycle为False时遍历工作不阻塞快速完成，recycle为True时遍历工作阻塞
       self.off = False

    # 文件（夹）找到时的回调函数
   class FinderCallback:
       # 找到文件夹
       def onFindDir(self,dir_path):
           pass
       # 找到文件
       def onFindFile(self,file_path,size):
           pass
       # 预留的刷新函数
       def onRefresh(self):
           pass

   # 查找文件（夹）方法
   def list_flie(self,root_dir):
       if  os.path.isfile(root_dir):
           while self.recycle:
               time.sleep(0.02)
           if self.finderCallback:
               self.finderCallback.onFindFile(root_dir,os.path.getsize(root_dir))
               self.finderCallback.onRefresh()
               if not self.off:
                  self.recycle = True
       else:
           list = os.listdir(root_dir)  # 列出文件夹下所有的目录与文件
           for i in range(0, len(list)):
               path = os.path.join(root_dir, list[i])
               if os.path.isfile(path):
                   while self.recycle:
                       time.sleep(0.02)
                   if self.finderCallback:
                       self.finderCallback.onFindFile(path,os.path.getsize(path))
                       self.finderCallback.onRefresh()
                       if not self.off:
                          self.recycle = True
               else:
                   while self.recycle:
                       time.sleep(0.02)
                   if self.finderCallback:
                       self.finderCallback.onFindDir(path)
                       self.finderCallback.onRefresh()
                       if not self.off:
                          self.recycle = True
                   # 递归调用（当遍历到文件夹时，继续遍历，直到当前文件夹下没有文件夹为止）
                   self.list_flie(path)

# 文件、文件夹寻找类2（快速寻找，无阻塞）
class FileFinder_Fast:
   def __init__(self,finderCallback):
       self.finderCallback = finderCallback
       self.debug = True
       # 文件（夹）路径下所有文件的总大小
       self.sum_size = 0

    # 文件（夹）找到时的回调函数
   class FinderCallback:
       # 找到文件夹
       def onFindDir(self,dir_path):
           pass
       # 找到文件
       def onFindFile(self,file_path,size):
           pass
       # 预留的刷新函数
       def onRefresh(self):
           pass

   def list_flie(self,root_dir):
       if  os.path.isfile(root_dir):
           if self.debug:print('Found File: %s' % root_dir)
           if self.finderCallback:
               self.finderCallback.onFindFile(root_dir,os.path.getsize(root_dir))
               self.finderCallback.onRefresh()
       else:
           list = os.listdir(root_dir)
           for i in range(0, len(list)):
               path = os.path.join(root_dir, list[i])
               if os.path.isfile(path):
                   if self.debug:print('Found File: %s' % path)
                   if self.finderCallback:
                       self.finderCallback.onFindFile(path,os.path.getsize(path))
                       self.finderCallback.onRefresh()
               else:
                   if self.finderCallback:
                       self.finderCallback.onFindDir(path)
                       self.finderCallback.onRefresh()
                   if self.debug:print('Found Dir: %s' % path)
                   self.list_flie(path)

class MyfinderCallback(FileFinder.FinderCallback):
    def onFindDir(self,dir_path):
        print(dir_path)
    def onFindFile(self,file_path,size):
        print('   ' + file_path + ' ' + str(size))


# if __name__ == '__main__':
#      finder = FileFinder(MyfinderCallback())
#      finder.recycle = False
#      finder.list_flie('/Users/capton/desktop/video_downloader')