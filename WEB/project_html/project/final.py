from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
import logging
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db_config = {
    'host': 'project-db-stu3.smhrd.com',
    'user': 'Insa4_IOTA_hacksim_5',
    'password': 'aishcool5',
    'database': 'Insa4_IOTA_hacksim_5',
    'port': 3307
}

db = mysql.connector.connect(**db_config)


def is_duplicate_id(admin_id):
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM admin WHERE ADMIN_ID = %s"
    cursor.execute(sql, (admin_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/login_page')
def index():
    return render_template('login1.html')


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
        return jsonify({"message": "로그인 성공."}), 200
    else:
        return jsonify({"message": "아이디 or 비밀번호가 올바르지 않습니다."}), 401


@app.route('/signup')
def signup_page():
    return render_template('register.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        admin_id = request.form['ADMIN_ID']
        admin_pw = request.form['ADMIN_PW']
        company = request.form['COMPANY']
        ph = request.form['PH']

        if is_duplicate_id(admin_id):
            return "이미 사용 중인 아이디입니다."

        cursor = db.cursor()
        sql = "INSERT INTO admin (ADMIN_ID, ADMIN_PW, COMPANY, PH) VALUES (%s, %s, %s, %s)"
        values = (admin_id, admin_pw, company, int(ph))

        cursor.execute(sql, values)
        db.commit()
        cursor.close()

        return redirect(url_for('signup_success'))  # 회원가입 성공 페이지로 리다이렉트


@app.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')  # 회원가입 성공 페이지 렌더링


@app.route('/check_id_duplicate/<admin_id>')
def check_id_duplicate(admin_id):
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM admin WHERE ADMIN_ID = %s"
    cursor.execute(sql, (admin_id,))
    count = cursor.fetchone()[0]
    cursor.close()

    if count > 0:
        return "duplicate"
    else:
        return "not_duplicate"


@app.route('/connect')
def connect():
    return render_template('connect.html')


def get_trash_capacity():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(buffered=True)

        query = "SELECT BIN_LEVEL FROM BIN_INFO ORDER BY M_NUM DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            capacity = result[0]
        else:
            capacity = "N/A"

        cursor.close()
        conn.close()

        return capacity
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        return "Error"


@app.route("/")
def index_trash():
    capacity = get_trash_capacity()
    return render_template("connect.html", capacity=capacity)


# MQTT 클라이언트 생성
mqtt_client = mqtt.Client()


# MQTT 브로커에 연결하는 콜백 함수
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# MQTT 클라이언트에 콜백 함수 등록
mqtt_client.on_connect = on_connect

# MQTT 브로커에 연결
mqtt_broker_address = "broker.hivemq.com"
mqtt_port = 1883
mqtt_client.connect(mqtt_broker_address, mqtt_port, 60)

# MQTT 클라이언트 루프 실행
mqtt_client.loop_start()


# MQTT 메시지 발행 함수
def publish_mqtt_message(value):
    mqtt_client.publish("maple/world", str(value))


# 쓰레기통 출발 처리 함수
@app.route("/start", methods=["POST"])
def start_trash():
    try:
        publish_mqtt_message(1)
        return jsonify({"message": "쓰레기통 출발이 요청되었습니다."}), 200
    except Exception as e:
        return jsonify({"message": "쓰레기통 출발 요청을 실패했습니다."}), 500


# 쓰레기통 멈춤 처리 함수
@app.route("/stop", methods=["POST"])
def stop_trash():
    try:
        publish_mqtt_message(0)
        return jsonify({"message": "쓰레기통 멈춤이 요청되었습니다."}), 200
    except Exception as e:
        return jsonify({"message": "쓰레기통 멈춤 요청을 실패했습니다."}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
