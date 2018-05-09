import requests,json,string,re
from bs4 import BeautifulSoup
from zhon.hanzi import punctuation

#对爬取的网页提取其中文本
def souhu_url(url):
    results = requests.get(url)
    results.encoding = results.encoding
    soup_texts = BeautifulSoup(results.text,'lxml')
    aa = soup_texts.find_all("p")
    text =''
    for i in aa:
        try:
            dd = str(i.contents[0])
            if 'src' not in dd and 'span' not in dd and 'strong' not in dd:   #去除一些标签
                text+=dd
        except Exception as e:
            pass
    return text

#保存爬取的数据到文件
def save_data(title,text):
    f = open('./news/%s.txt'%(title),'w',encoding='utf8')
    f.write(text)
    f.close()

#0305
lis=['0327','0326','0325','0324','0323','0322','0321','0320','0319','0318','0317','0316','0315','0314','0313','0312','0311','0310','0309','0308','0307','0306','0305','0304','0303','0302','0301']
for ii in lis:
    url_sohu = 'http://news.sohu.com/_scroll_newslist/2018%s/news.inc'%(ii)
    results = requests.get(url_sohu)
    results.encoding='utf8'
    #为转化成json数据做处理
    t = results.text[16:]
    t = t.replace('category', '\"category\"')
    t = t.replace('item', '\"item\"')
    te = json.loads(t)

    count=0
    dic ={0:"国内",1:"国际",2:"社会",3:"财经",4:"军事",5:"体育",6:"娱乐",7:"文化",8:"汽车"}
    for i in te['item']:
        try:
            category = dic[i[0]]
            title = i[1]  #提取标题
            url = i[2]    #提取网址
            text = souhu_url(url)
            text = text.strip()
            if len(text)<100:
                continue
            delset = string.punctuation
            title = re.sub(u"[%s]+" % delset, "", title)#去除英文标点
            title = re.sub(u"[%s]+" % punctuation, "", title) #去除中文标点
            title = '['+str(category)+']'+str(title)
            save_data(title,text)
            count+=1
        except Exception as e:
            print(e)
    print(ii,count)

