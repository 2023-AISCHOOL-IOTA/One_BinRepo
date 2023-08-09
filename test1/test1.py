from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL 연결 설정
db = mysql.connector.connect(
    host="project-db-stu3.smhrd.com",
    user="Insa4_IOTA_hacksim_5",
    password="aishcool5",
    database="Insa4_IOTA_hacksim_5",
    port = 3307
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('test1.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['ADMIN_ID']  # 폼 필드의 이름과 일치하는 키 사용
    password = request.form['ADMIN_PW']  # 폼 필드의 이름과 일치하는 키 사용
    company = request.form['COMPANY']  # 폼 필드의 이름과 일치하는 키 사용
    phone = request.form['PH']  # 폼 필드의 이름과 일치하는 키 사용

    # MySQL에 데이터 저장
    query = "INSERT INTO admin (ADMIN_ID, ADMIN_PW, COMPANY, PH) VALUES (%s, %d, %s, %d)"
    values = (name, password, company, phone)
    cursor.execute(query, values)
    db.commit()

    return "회원가입이 완료되었습니다."

if __name__ == '__main__':
    app.run()
