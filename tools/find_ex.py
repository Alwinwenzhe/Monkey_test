#!/usr/bin/env python
#coding:utf8

import os
import re

regtxt = r'.+?\.txt' #扫描对象为txt文件.
regcontent = r'what is your name' #列出内容含有'what is your name'的文件

class FileException(Exception):
    pass

def getdirlist(filepath):
    """获取目录下所有的文件."""

    txtlist = [] #文件集合.
    txtre = re.compile(regtxt)
    needfile = [] #存放结果.
    for parent, listdir, listfile in os.walk(filepath):
        for files in listfile:
            #获取所有文件.
            istxt = re.findall(txtre, files)
            filecontext = os.path.join(parent, files)
            #获取非空的文件.
            if istxt :
                txtlist.append(filecontext)
                #将所有的数据存放到needfile中.
                needfile.append(readfile(filecontext))

    if needfile == []:
        raise FileException("no file can be find!")
    else:
        validatedata = getvalidata(needfile)
        print (validatedata)
        print ('total file %s , validate file %s.' %(len(txtlist),len(validatedata)))

def getvalidata(filelist=[]):
    """过滤集合中空的元素."""

    valifile = []
    for fp in filelist:
        if fp != None:
            valifile.append(fp)
    return valifile

def readfile(filepath):
    """通过正则匹配文本中内容，并返回文本."""

    flag = False
    contentre = re.compile(regcontent)
    fp = open(filepath, 'a+')
    lines = fp.readlines()
    flines = len(lines)
    #逐行匹配数据.
    for i in range(flines):
        iscontent = re.findall(contentre, lines[i])
        if iscontent:
            fp.close()
            return filepath

if __name__ == "__main__":
    getdirlist('C:\python27')