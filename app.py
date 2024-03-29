from sentiment import analysis
from getcomment import getcomment
from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analysis',methods = ['POST'])
def main():
    url = request.form['url']
    comments,status = getcomment(url)
    if status == 1:
        return "目前不支持这个网站 "
    elif status == 2:
        return "此链接不合法"
    elif status == 3:
        return "没有评论"
    elif status == 0:
        # print(comments)
        return render_template('analysis.html',data=analysis(comments))
@app.route('/help')
def help():
    return render_template('site/index.html')
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)