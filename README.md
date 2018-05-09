# simple_search_engine  
# 本项目是基于Python的Flask框架搭建的简易搜索引擎  
## 运行方法：
1. 安装python3.6  
2. 执行pip install requirements.txt (requirements中包含了本项目所引用的包，主要是分词和flask框架）  
## 项目文件：  
### 文件：  
* search_engine.py  项目启动文件，主要是Flask的启动，函数为网页后端的操作函数  
* sentence_similarity.py 句子相似性计算，提供main函数接口支持其他文件调用  
* vsm_search_engines.py  搜索引擎的实现，输入句子找出最相似的文章，提供main函数接口支持其他文件调用  
* TF_IDF.py          所有文章中每个词TF_IDF的计算，提供main函数接口支持其他文件调用  
* util.py            一些在多个文件中都会用到的工具函数，可直接调用  
* news_scrapy.py     搜狐新闻的爬取，爬取后的新闻存到news文件夹  
* test.py            测试一些函数功能  
* stopsword.txt      停用词的表  
* requirements.txt   需要包的集合  
* Readme             项目说明  
### 文件夹：  
* news               爬取的最原始的语料  
* segfile            分词之后的语料  
* tfidffile          每个新闻中每个词的TFIDF  
* static             主要包括网页的样式和一些资源  
* templates          网页的模板，其中SIM.html为计算句子相似性，SJet.html为搜索引擎   
## 项目启动:  
1. 运行search_engine.py文件  
2. 在浏览器输入127.0.0.1:5000/可进入计算句子相似性页面  
3. 在浏览器输入127.0.0.1:5000/search 可进入搜索引擎页面  

