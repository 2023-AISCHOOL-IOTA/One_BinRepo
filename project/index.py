from flask import Flask, render_template
import db

app = Flask(__name__)



@app.route('/')
def index():
    # templates 폴더내의 html문서 탐색
    # index.css 처럼 html 아닌것들은 전부 static 폴더에 넣는다
    return render_template('index.html')

@app.route('/test')
def test():

    result = db.select_admin()
    result = str(result)
    return result

@app.route('/table')
def table():

    result = db.select_admin()
    name = result[0][0]
    pw = result[0][1]
    company = result[0][2]
    ph = result[0][3]
    print(name, pw, company, ph)
    return render_template('index2.html', name=name, pw=pw, company=company, ph=ph)


if __name__ == '__main__':
    app.run('0.0.0.0', 5021)