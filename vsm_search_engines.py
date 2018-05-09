import importlib,sys,math
importlib.reload(sys)
import jieba,os

from util import getFilelist,delete_symbol
from TF_IDF import cal_idf
allpath = str(os.getcwd()).replace('\\','/')
#allpath ='C:/Users/zhou/PycharmProject/search_engine'

#传入分完词计算完TFIDF的文档,默认选出前20的关键词
def find_keywords(seg_text,words_num = 20):
    f = open(seg_text,'r+')
    dic = {}
    for line in f.readlines():
        word = line.strip().split(' ')
        dic[word[0]] = float(word[1])
    f.close()
    dic = sorted(dic.items(), key=lambda asd: asd[1], reverse=True)
    if len(dic)>20:
        return dic[:20]
    else:
        return dic

#根据关键词计算二者余弦相似度
def MergeKeys(dic1, dic2):

    arrayKey = []
    for i in range(len(dic1)):
        arrayKey.append(dic1[i][0])  # 向数组中添加元素
    for i in range(len(dic2)):
        if dic2[i][0] not in arrayKey:
            arrayKey.append(dic2[i][0])
    #print(arrayKey)
    # 计算词频 infobox可忽略TF-IDF
    arrayNum1 = [0] * len(arrayKey)
    arrayNum2 = [0] * len(arrayKey)

    # 赋值arrayNum1
    for i in range(len(dic1)):
        key = dic1[i][0]
        value = dic1[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                arrayNum1[j] = value
                break
            else:
                j = j + 1
    # 赋值arrayNum2
    for i in range(len(dic2)):
        key = dic2[i][0]
        value = dic2[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                arrayNum2[j] = value
                break
            else:
                j = j + 1

    # 计算两个向量的点积
    x = 0
    i = 0
    while i < len(arrayKey):
        x = x + arrayNum1[i] * arrayNum2[i]
        i = i + 1

    # 计算两个向量的模
    i = 0
    sq1 = 0
    while i < len(arrayKey):
        sq1 = sq1 + arrayNum1[i] * arrayNum1[i]  # pow(a,2)
        i = i + 1

    i = 0
    sq2 = 0
    while i < len(arrayKey):
        sq2 = sq2 + arrayNum2[i] * arrayNum2[i]
        i = i + 1

    result = float(x) / (math.sqrt(sq1) * math.sqrt(sq2))
    return result

#对query做处理，分词，计算每个值TFIDF值
def sentence_process (sen,allfile):
    path='/segfile/'
    filenum =len(allfile)
    sen = list(jieba.cut(delete_symbol(sen)))   #对删除标点的句子分词
    dic = {}
    for i in sen: #计算TF
        if i in dic.keys():
            dic[i]+=1
        else:
            dic[i] = 1
    for i in dic: #计算TFIDF
        count = 0
        for j in allfile:
            f = open(allpath+path+j,'r+')
            text =f.read()
            if i in text.split(' '):
                count+=1
            f.close()
        dic[i] = dic[i] * cal_idf(count,filenum)
    dic = sorted(dic.items(), key=lambda asd: asd[1], reverse=True)
    return dic


def main(sen,tfidf_path =allpath+'/tfidffile' ):#找出与sen最相关的前10条新闻
    allfile = getFilelist(tfidf_path) #获得所有的文件名
    scores = {}
    dic3 = sentence_process(sen, allfile)  # 查询语句的关键词
    for file in allfile:
        try:
            dic1 = find_keywords(tfidf_path+'/'+file)  #求文件的关键词
            score = MergeKeys(dic1, dic3)
            scores[file] = score
        except Exception:
            pass
    scores = sorted(scores.items(), key=lambda asd: asd[1], reverse=True) #排序
    result = []
    for i in scores:
        result.append(i[0])
    return result[:10]

if __name__ == '__main__':
    sen = '2月BHI全国建材家居景气指数再现下降'
    print(main(sen))
