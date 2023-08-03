#1. JS 사용 데이터 동적으로 로딩
#2. HTML 변수 활용 

import pymysql as ps

def select_admin():
    conn = ps.connect(host='project-db-stu3.smhrd.com',
                    user='Insa4_IOTA_hacksim_5',
                    passwd='aishcool5',
                    db='Insa4_IOTA_hacksim_5',
                    port=3307)

    curs = conn.cursor()
    sql = 'select * from admin'
    curs.execute(sql)

    # insert, update, delete
    # conn.commit()

    result = curs.fetchall()

    # 열었던 통로 역순 닫기
    curs.close()
    conn.close()

    return result



