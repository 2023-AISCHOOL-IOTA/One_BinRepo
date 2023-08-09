from flask import Flask, render_template, request, jsonify
from flask import redirect
import mysql.connector

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db_config = {
    'host': 'project-db-stu3.smhrd.com',
    'user': 'Insa4_IOTA_hacksim_5',
    'password': 'aishcool5',
    'database': 'Insa4_IOTA_hacksim_5',
    'port': 3307
}

@app.route('/')
def index():
    return render_template('login1.html')  # HTML 파일 이름


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT * FROM admin WHERE ADMIN_ID = %s AND ADMIN_PW = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
         return redirect('/connect1')
    else:
        return jsonify({"message": "아이디 또는 비밀번호가 올바르지 않습니다."})
    
@app.route('/connect1')
def connect1():
    return render_template('connect1.html') # connect1.html 파일 렌더링


if __name__ == '__main__':
    app.run(debug=True)
