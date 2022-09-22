'''
Created on 2022年9月21日

@author: 云
'''
import re, sys, datetime

def getText(path):#通过地址，读入文档
    file = open(path,'r',encoding = 'utf-8')#打开文件
    texts = file.readlines()#读取所有行
    file.close()#关闭文件
    return texts
    
def is_Chinese(word):#判断是否为中文
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def msplit(s, seperators = ',|\.|\?|，|。|？|！'):#将段落分成句子
    return re.split(seperators, s)

def readDocx(docfile):#对文本内容进行分割
    print('*' * 80)
    print('文件', docfile, '加载中……')
    t1 = datetime.datetime.now()
    paras = getText(docfile)
    segs = []
    for p in paras:
        temp = []
        for s in msplit(p):
            if len(s) > 2: #引用msplit方法将段落分为句子
               temp.append(s.replace(' ', "")) #将空格等替换掉并拼凑在temp里

        if len(temp) > 0:
            segs.append(temp)
    t2 = datetime.datetime.now()#记录完成时间
    print('加载完成，用时: ', t2 - t1)
    showInfo(segs, docfile)#展示相关信息
    return segs

def showInfo(doc, filename = 'filename'):#展示文本相关信息
    chars = 0
    segs = 0
    for p in doc:
        for s in p:
            segs = segs + 1
            chars = chars + len(s)
    print('段落数: {0:>8d} 个。'.format(len(doc)))
    print('短句数: {0:>8d} 句。'.format(segs))
    print('字符数: {0:>8d} 个。'.format(chars))
    


def compareParagraph(doc1, i, doc2, j, min_segment = 3): #核心算法，功能为比较两个段落的相似度，返回结果为两个段落中相同字符的长度与较短段落长度的比值。
    #param min_segment = 3: 最小段的长度，小于3的不判定是否为抄袭
       
    p1 = doc1[i]
    p2 = doc2[j]
    len1 = sum([len(s) for s in p1])
    len2 = sum([len(s) for s in p2])
    #如果两个段落的字符数量有一个小于10，则不认为有抄袭可能
    if len1 < 10 or len2 < 10:
        return []
    
    list_p = []
    for s1 in p1:
        if len(s1) < min_segment:#判断段落是否可以构成抄袭，不构成则跳出该循环
            continue;
        for s2 in p2:
            if len(s2) < min_segment:
                continue;
            if s2 in s1:#构成抄袭则拼接在list_p中
                list_p.append(s2)
            elif s1 in s2:
                list_p.append(s1)
                       
    # 取两个字符串的最短的一个进行比值计算
    count = sum([len(s) for s in list_p])
    ratio = float(count) /  min(len1, len2)
    if count > 10 and ratio > 0.1:#若抄袭的数量超过十则展示
        print(' 发现相同内容 '.center(80, '*'))
        print('文件1第{0:0>4d}段内容：'.format(i + 1))
        print('文件2第{0:0>4d}段内容：'.format(j + 1))
       # print('相同内容：', list_p)
        print('相同字符比：{1:.2f}%\n相同字符数： {0}\n'.format(count, ratio * 100))
    return list_p
 
if len(sys.argv) < 4:#如果在cmd没有输入三个文件
    print("参数小于3.")

doc1 = readDocx(sys.argv[1])#在cmd读入文件一
doc2 = readDocx(sys.argv[2])#在cmd读入文件二
#记录文件一的字符数
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
doc3 = sys.argv[3]#获得answer文件的绝对路径
with open(doc3,"w") as f:
    f.write("文章相似百分比为：")
    f.write(m2)
    print("文件写入完成")
