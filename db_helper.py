"""
    论坛数据库帮手类
        封装数据库的基本操作：
        连接数据库，关闭连接，执行查询，执行增删改，清除数据库
"""
"""
数据库: forum  用户数据表：users
"""


from conn_db import *
import pymysql


class DBConnector:
    """
        数据库帮手类
    """
    def __init__(self):
        """
           数据库助手类的构造函数：数据库连接对象
        """
        self.__conn=None
        self.open_conn()

    # 连接数据库
    def open_conn(self):
        """
            连接数据库
        :return: 无
        """
        try:
            self.__db_conn=pymysql.connect(host, user, password, database)
        except Exception as e:
            print(e)

    # 关闭数据库
    def close_conn(self):
        """
            关闭数据库
        :return: 无
        """
        try:
            self.__db_conn.close()
        except Exception as e:
            print("关闭数据库错误")
            print(e)
        else:
            print("关闭数据库成功")

    # 执行查询
    def do_select(self,sql):
        """
            执行数据库查询操作
        :param sql: sql语句，type:pymysql
        :return: 返回结果集
        """
        cursor=self.__db_conn.cursor()    # 获取游标
        try:
            cursor.execute(sql)     # 执行sql语句
        except Exception as e:
            print("执行查询错误,原因是",e)
            return None   # 执行失败则返回空对象
        else:
            result=cursor.fetchone()    #提取所有数据
            cursor.close()      # 关闭游标
            return result      # 返回查询结果

    # 执行修改
    def do_update(self,sql):
        """
            执行数据库增删改操作
        :param sql: sql语句，type:pymysql
        :return: 返回受影响笔数
        """
        cursor = self.__db_conn.cursor()  # 创建游标
        try:
            result=cursor.execute(sql)     # 执行sql语句
        except Exception as e:
            self.__db_conn.rollback()     # 出错则回滚
            print("执行更新错误，原因是",e)
            return None     # 返回空对象
        else:
            self.__db_conn.commit()  # 提交事务
            cursor.close()  # 关闭游标
            return result  # 返回受影响笔数


    # 执行查询返回多个结果
    def do_select_many(self,sql):
        """
            执行数据库查询操作
        :param sql: sql语句，type:pymysql
        :return: 返回结果集
        """
        cursor=self.__db_conn.cursor()    # 获取游标
        try:
            cursor.execute(sql)     # 执行sql语句
        except Exception as e:
            print("执行查询错误,原因是",e)
            return None   # 执行失败则返回空对象
        else:
            result=cursor.fetchall()    #提取所有数据
            cursor.close()      # 关闭游标
            return result      # 返回查询结果

    def clear_database(self):
        sql = "delete from users;"
        cursor = self.__db_conn.cursor()
        result = cursor.execute(sql)
        return result

if __name__=="__main__":
    # 测试查询函数
    dbhelper=DBConnector()     # 实例化数据库对象
    # dbhelper.clear_database()
    sql="insert into users values(1,'alex','123',now(),0)"
    result=dbhelper.do_update(sql)    # 执行增加数据
    print(result)
    dbhelper.close_conn()   # 关闭数据库连












