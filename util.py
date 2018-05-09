import os,string
from zhon.hanzi import punctuation

def getFilelist(path):
    filelist = []
    files = os.listdir(path)
    for f in files:
        if (f[0] == '.'):
            pass
        else:
            filelist.append(f)
    return filelist

def delete_symbol(title):#删除一个句子中标点
    delset = string.punctuation
    for i in delset:
        if i in str(title):
            title = title.replace(i,'')
    for i in punctuation:
        if i in str(title):
            title = title.replace(i,'')
    return str(title)