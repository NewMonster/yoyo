"""
    论坛数据库登录信息模块
"""
import pymysql


host="localhost"
user="root"
password="123456"
database="forum"


def do_erro():
    conn=pymysql.connect(host, user, password, database)
    cursor=conn.cursor()
    sql="update users set status=0 where status=1"
    r=cursor.execute(sql)
    conn.commit()
    print(r)
    cursor.close()
    conn.close()


if __name__=="__main__":
    do_erro()