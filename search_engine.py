from flask import Flask,render_template,request,flash,session
import os
from sentence_similarity import main as sen_simi
from vsm_search_engines import main as search_eng
from TF_IDF import main as tfidfmain

app = Flask(__name__)
path="C:/Users/zhou/PycharmProject/search_engine/tfidffile/"

def process_text(name):
    f = open(path + name, 'r')
    ss = ''
    for i in f.readlines():
        i = i.replace(' ', ':')
        ss = ss + i.strip() + ' '
    f.close()
    return ss

@app.route('/')
def hello_world():
    return render_template('SIM.html')

@app.route('/auth_page', methods=['GET', 'POST'])
def auth_page():
    if request.method=='POST':
        sen1 = str(request.values.get("first"))
        sen2 = str(request.values.get("last"))
        dot,cos,jaccard = sen_simi(sen1,sen2)
        return render_template('SIM.html',dot = str(dot),cos =str(cos),jaccard =str(jaccard),sen1 =sen1,sen2=sen2)
    else:
        return render_template('SIM.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        query = request.values.get("query")
        results = search_eng(query)
        return render_template('SJet.html',results = results)
    else:
        return render_template('SJet.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            f = request.files['file']
            basepath = os.path.dirname(__file__)  # 当前文件所在路径
            upload_path = os.path.join(basepath, 'news',f.filename)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            session['filename'] = f.filename
            return render_template('SIM.html',success=1)
        except Exception:
            return render_template('SIM.html',success=0)

@app.route('/cal_show', methods=['GET','POST'])
def cal_show():
    filename = session.get('filename')
    if filename:
        tfidfmain(filename)
        content =process_text(filename)
        return render_template('SIM.html',content=content)
    else:
        return render_template('SIM.html')

if __name__ == '__main__':
    key = os.urandom(24)
    app.config['SECRET_KEY'] = key
    app.run()
