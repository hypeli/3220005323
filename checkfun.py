'''
Created on 2022年9月21日

@author: 云
'''
#coding=utf-8

#from docx import Document
import re, sys, datetime
from sys import argv
from _sqlite3 import Row

def getText(path):#读入文档
    texts = []
    file = open(path,'r',encoding = 'utf-8')#打开文件
    #texts = file.readlines()#读取所有行
    texts = file.readlines()#读取所有行
   # for Row in file_data:
   #     tmp_list = Row.split(' ')#按‘，’切分每行数据
   #     tmp_list[-1] = tmp_list[-1].replace("\n",',')#去掉换行符
   #     texts.append(tmp_list)#拼接文本
    file.close()#关闭文件
    return texts
    
    
def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def msplit(s, seperators = ',|\.|\?|，|。|？|！'):
    return re.split(seperators, s)

def readDocx(docfile):
    print('*' * 80)
    print('文件', docfile, '加载中……')
    t1 = datetime.datetime.now()
    paras = getText(docfile)
    segs = []
    for p in paras:
        temp = []
        for s in msplit(p):
            if len(s) > 2:
               temp.append(s.replace(' ', ""))
              # temp.append(s)
        if len(temp) > 0:
            segs.append(temp)
    t2 = datetime.datetime.now()
    print('加载完成，用时: ', t2 - t1)
    showInfo(segs, docfile)
    return segs

def showInfo(doc, filename = 'filename'):
    chars = 0
    segs = 0
    for p in doc:
        for s in p:
            segs = segs + 1
            chars = chars + len(s)
    print('段落数: {0:>8d} 个。'.format(len(doc)))
    print('短句数: {0:>8d} 句。'.format(segs))
    print('字符数: {0:>8d} 个。'.format(chars))
    


def compareParagraph(doc1, i, doc2, j, min_segment = 3): 
    """
    功能为比较两个段落的相似度，返回结果为两个段落中相同字符的长度与较短段落长度的比值。
    :param p1: 行
    :param p2: 列
    :param min_segment = 5: 最小段的长度
    """
    p1 = doc1[i]
    p2 = doc2[j]
    len1 = sum([len(s) for s in p1])
    len2 = sum([len(s) for s in p2])
    #
    if len1 < 10 or len2 < 10:
        return []
    
    list_p = []# @ReservedAssignment
    for s1 in p1:
        if len(s1) < min_segment:
            continue;
        for s2 in p2:
            if len(s2) < min_segment:
                continue;
            if s2 in s1:
                list_p.append(s2)
            elif s1 in s2:
                list_p.append(s1)
                       
    # 取两个字符串的最短的一个进行比值计算
    count = sum([len(s) for s in list_p])
    ratio = float(count) /  min(len1, len2)
    if count > 10 and ratio > 0.1:
        print(' 发现相同内容 '.center(80, '*'))
       # print('文件1第{0:0>4d}段内容：{1}'.format(i + 1, p1))
       # print('文件2第{0:0>4d}段内容：{1}'.format(j + 1, p2))
       # print('相同内容：', list_p)
        print('相同字符比：{1:.2f}%\n相同字符数： {0}\n'.format(count, ratio * 100))
    return list_p
 
if len(sys.argv) < 3:
    print("参数小于2.")

doc1 = readDocx(sys.argv[1])
doc2 = readDocx(sys.argv[2])
chars = 0
for p in doc1:
        for s in p:
            chars = chars + len(s)

print('开始比对...'.center(80, '*'))
t1 = datetime.datetime.now()
m = 0
for i in range(len(doc1)):
    if i % 100 == 0:
        print('处理进行中')
    for j in range(len(doc2)):
        compareParagraph(doc1, i, doc2, j)
        m = m +len(compareParagraph(doc1, i, doc2, j))#记录文章相同内容的数目
        
ratio = float(m) /  chars#计算百分百比
m1 = 0
m2 = 0
#四舍五入
m1 = round(float(ratio) *100,2)
m2 = "%.2f%%" % m1
print(m2)