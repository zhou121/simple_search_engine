import os
import jieba
import math
import importlib,sys
importlib.reload(sys)
from util import getFilelist
allpath ='C:/Users/zhou/PycharmProject/search_engine'
#获得停用词表
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords



# 对文档进行分词处理
def fenci(argv, path=allpath+"/news/"):
    # 保存分词结果的目录
    sFilePath = allpath+'/segfile'
    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)
    # 读取文档

    filename = argv
    f = open(path + filename, 'r+',encoding='utf8')
    file_list = f.read()
    f.close()

    # 对文档进行分词处理，采用默认模式
    sentence_seged = jieba.cut(file_list.strip(),cut_all=True)
    stopwords = stopwordslist(allpath+'/stopsword.txt')  # 这里加载停用词的路径
    outstr = [w for w in sentence_seged if not w in stopwords]


    # 对空格，换行符进行处理
    result = []
    for seg in outstr:
        seg = ''.join(seg.split())
        if (seg != '' and seg != "\n" and seg != "\n\n"):
            result.append(seg)

# 将分词后的结果用空格隔开，保存至本地。比如"我来到北京清华大学"，分词结果写入为："我 来到 北京 清华大学"
    print('save  ',filename)
    f = open(sFilePath + "/" + filename, "w+")
    f.write(' '.join(result))
    f.close()

#词频统计
def wordcount(text):
    lis = text.split(' ')
    dic = {}
    for i in lis:
        if i in dic.keys():
            dic[i]+=1
        else:
            dic[i]=1
    return dic

#IDF计算
def cal_idf(num,allnum):
    return math.log(allnum / (1 + num))

# 读取已分词好的文档，进行TF-IDF计算
def Tfidf(filelist):
    path =allpath+ '/segfile/'
    corpus = []  # 取文档的分词结果
    for ff in filelist:
        fname = path + ff
        f = open(fname, 'r+')
        content = f.read()
        f.close()
        corpus.append(content)
    idf ={} #存储所有文档中相应词出现的频率
    tf =[]  #存储每篇文档每个词的TF值
    for i in corpus:
        dic={}
        num = len(i.split(' '))
        for k,v in wordcount(str(i)).items():
            dic[k] = v/num  #计算词的TF
            if k in idf.keys():
                idf[k]+=1
            else:
                idf[k] =1
        tf.append(dic)
    allnum = len(filelist)
    tfidf=[] #计算每篇文档每个词的TFIDF值
    for i in tf:
        dic={}
        for k,v in i.items():
            dic[k] = v * cal_idf(idf[k],allnum)
        tfidf.append(dic)


    sFilePath =allpath+ '/tfidffile'
    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)

    # 这里将每份文档词语的TF-IDF写入tfidffile文件夹中保存
    for i in range(len(filelist)):
        print("--------Writing all the tf-idf in the", i, u" file into ", sFilePath + '/' + filelist[i], "--------")
        f = open(sFilePath + '/' +filelist[i], 'w+')
        for k,v in tfidf[i].items():
            ss = str(k)+' '+str(v)+'\n'
            f.write(ss)
        f.close()

def main(filename):
    news_path = allpath+"/segfile/"
    fenci(filename)
    allfile= getFilelist(news_path)
    Tfidf(allfile)


if __name__ == "__main__":
    # news_path = "./news/"
    # allfile= getFilelist(news_path)
    # for ff in allfile:
    #     fenci(ff, news_path)
    # Tfidf(allfile)
    main('1.txt')