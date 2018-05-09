import chardet
path="C:/Users/zhou/PycharmProject/search_engine/tfidffile/"
f=open(path+'[财经]2月BHI全国建材家居景气指数再现下降.txt','r')
ss = ''
for i in f.readlines():
    # f_charInfo = chardet.detect(i)
    # i = i.decode(f_charInfo['encoding'])
    i=i.replace(' ',':')
    ss=ss+i.strip()+' '

print(ss)
f.close()
