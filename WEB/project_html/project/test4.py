from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host='project-db-stu3.smhrd.com',
    user='Insa4_IOTA_hacksim_5',
    passwd='aishcool5',
    db='Insa4_IOTA_hacksim_5',
    port=3307
)

@app.route('/')
def index():
    return render_template('index4.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        admin_id = request.form['ADMIN_ID']
        admin_pw = request.form['ADMIN_PW']
        company = request.form['COMPANY']
        ph = request.form['PH']

        cursor = db.cursor()
        sql = "INSERT INTO admin (ADMIN_ID, ADMIN_PW, COMPANY, PH) VALUES (%s, %s, %s, %s)"
        values = (admin_id, admin_pw, company, int(ph))
        
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

        return "회원가입이 성공적으로 완료되었습니다."

if __name__ == '__main__':
    app.run(debug=True)
