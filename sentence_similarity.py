import jieba
import numpy
from util import delete_symbol

#句子embedding
def sentence_embedding(sen_list):#句子的编码，这里传入句子的集合
    words = [] #存储所有分完词的句子
    emdedding_words=[] #存储最终的embedding后的对应的单词顺序
    for sen in sen_list: #分词
        lis = list(jieba.cut(delete_symbol(sen)))
        words.append(lis)
        for i in lis:
            if i not in emdedding_words:
                emdedding_words.append(i)
    #print(emdedding_words)
    emdedding_sen = [] #编码好的句子
    for sen in words:
        #print(sen)
        vector = []
        for i in emdedding_words:#有该单词即为1
            if i in sen:
                vector.append(1)
            else:
                vector.append(0)
        emdedding_sen.append(vector)
    return emdedding_sen

#点积
def dot_product(a,b):#点积
    return numpy.dot(a,b)

#余弦相似度
def cos_similarity(A,B):
    num = numpy.dot(A,B)
    denom = numpy.linalg.norm(A) * numpy.linalg.norm(B)
    cos = num / denom  # 余弦值
    return cos

#jaccard 相似度计算
def jaccard(A,B):
    M11 = 0
    for i in range(len(A)):
        if A[i]==1 and B[i]==1:
            M11+=1
    return (M11)/len(A)

def main(sen1,sen2):#计算两个句子相似性
    sens = sentence_embedding([sen1,sen2])
    sen1 = numpy.array(sens[0])
    sen2 = numpy.array(sens[1])
    return dot_product(sen1,sen2),cos_similarity(sen1,sen2),jaccard(sen1,sen2)

if __name__ == '__main__':
    sen1 ='今天是晴天'
    sen2 = '小红最喜欢小明，特别的喜欢.'
    print(main(sen1,sen2))

