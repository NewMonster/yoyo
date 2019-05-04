"""
    电子词典服务端
"""
import signal,os,sys
from socket import *

import db_helper


HOST="127.0.0.1"
PORT=8000
ADDR=(HOST,PORT)


# 搭建网络连接
def main():
    # 创建套接字
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    print("waiting for the port 8000.....")

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    # 循环等待客户端连接
    while True:
        try:
            c,addr=s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        print("connect from:", addr)

        # 创建子进程
        pid=os.fork()
        if pid==0:
            s.close()
            # 子进程执行处理客户端请求
            log_request(c,addr)
            sys.exit()
        else:
            c.close()


# 子进程函数，处理登录，注册以及个人信息相关的客户端请求
def log_request(c,addr):
    # 创建处理一级页面请求对象
    handle_request=HandleRequest(c)
    while True:
        # 接收客户端请求
        data=c.recv(1024).decode()
        # 表示客户端退出的情况
        if not data or data[0]=="Q":
            print("break connect from",addr)
            c.close()
            return
        # 注册请求
        elif data[0]=="R":
            handle_request.do_register(data)
        # 登录请求
        elif data[0]=="L":
            handle_request.do_log(data)
        # 注销请求
        elif data[0]=="O":
            handle_request.do_logout(data)
        # 更改用户名请求
        elif data[0]=="N":
            handle_request.do_modify_name(data)
        # 更改密码请求
        elif data[0]=="P":
            handle_request.do_modify_password(data)

# 处理客户端请求类
class HandleRequest:
    def __init__(self,c):
        # 连接网络
        self.c=c
        self.db= db_helper.DBConnector()

    # 处理注册请求,加入用户数据到数据库
    def do_register(self,data):
        user_list=data.split(" ")
        name=user_list[1]
        password=user_list[2]
        sql="select * from users where name='%s'"%name
        r=self.db.do_select(sql)
        if r!=None:
            self.c.send("该用户已存在".encode())
            return
        elif r==None:
            self.c.send(b"ok")
            sql = "insert into users (name,password,register_time,status) values ('%s','%s',now(),1)" % (name, password)
            self.db.do_update(sql)
        else:
            self.c.send("注册失败".encode())

    # 处理登录请求,判断结果返回,成功则进入二级页面
    def do_log(self,data):
        user_list = data.split(" ")
        name = user_list[1]
        password = user_list[2]
        sql = "select * from users where name='%s'" % name
        r = self.db.do_select(sql)
        if r== None:
            self.c.send("用户名不存在,请确认或注册".encode())
            return
        # 如果用户存在，进行密码和状态判断
        else:
            # 如果密码不正确
            if r[2]!=password:
                self.c.send("密码错误,请重新输入".encode())
            # 如果密码正确，判断状态
            else:
                # 判断状态是否为登录中１，禁言２，封号３
                if r[4] in [1,2,3]:
                    self.c.send("用户已登录或用户状态异常,请联系管理员".encode())
                # 如果状态为０，发送ok给客户端，更改用户状态为登录中
                else:
                    self.c.send(b"ok")
                    sql = "update users set status=1 where name='%s'" % name
                    self.db.do_update(sql)

    # 处理退出请求,更改用户状态
    def do_logout(self,data):
        user_list = data.split(" ")
        name = user_list[1]
        sql = "update users set status=0 where name='%s'" %name
        self.db.do_update(sql)

    # 处理更改用户请求
    def do_modify_name(self,data):
        user_list = data.split(" ")
        name = user_list[1]
        sql="select * from users where name='%s'"%name
        result=self.db.do_select(sql)
        if result==None:
            self.c.send("错误，用户不存在，请确认".encode())
            return
        if result[4]!=1:
            self.c.send("用户状态异常，此操作违法".encode())
            return
        self.c.send(b"ok")
        mf_name=self.c.recv(128).decode()
        sql = "select * from users where name='%s'" % mf_name
        result = self.db.do_select(sql)
        if result==None:
            sql = "update users set name='%s' where name='%s'" %(mf_name,name)
            result = self.db.do_update(sql)
            if result!=None:
                self.c.send(b"ok")
            else:
                self.c.send("服务器错误，请联系管理员".encode())
        else:
            self.c.send("用户名重复，请重新输入".encode())


    # 处理更改用户密码请求
    def do_modify_password(self,data):
        user_list = data.split(" ")
        name = user_list[1]
        sql = "select * from users where name='%s'" % name
        result = self.db.do_select(sql)
        if result == None:
            self.c.send("错误，用户不存在，请确认".encode())
            return
        if result[4] != 1:
            self.c.send("用户状态异常，此操作违法".encode())
            return
        self.c.send(b"ok")
        mf_password = self.c.recv(128).decode()
        sql = "update users set password='%s' where name='%s'" % (mf_password, name)
        result = self.db.do_update(sql)
        if result != None:
            self.c.send(b"ok")
        else:
            self.c.send("服务器错误，请联系管理员".encode())





if __name__=="__main__":
    main()
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
    # 如果服务器异常则更改所有状态为１的用户状态为０
    sql = "update user set status=0 where status=1"
    db_helper.DBConnector().do_select(sql)




