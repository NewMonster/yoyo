"""
    电子词典 客户端
"""
from socket import *
import sys
import getpass
import db_helper

ADDR=("127.0.0.1",8000)

user_name=""

#创建一级页面--处理登录和注册以及退出
def main():
    # 搭建网络连接
    s=socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        sys.exit(e)
    log_mian=LogMain(s)
    while True:
        print("""
================Welcome===============
--1.注册        2.登录         3.退出--""")
        cmd=input("输入选项:")
        if cmd not in ["1","2","3"]:
            print("请输入正确选项")
        elif cmd=="1":
            log_mian.do_register()
        elif cmd=="2":
            log_mian.do_log()
        elif cmd=="3":
            log_mian.do_quit()

# 一级页面类
class LogMain:
    def __init__(self,s):
        self.s=s

    # 处理一级页面注册请求
    def do_register(self):
        while True:
            name=input("姓名:")
            password=getpass.getpass("密码:")
            password1 = getpass.getpass("确认密码:")
            if (" " in name) or (" " in password):
                print("用户名密码不能有空格")
                continue
            if password!=password1:
                print("两次输入密码不一致")
                continue
            msg="R %s %s"%(name,password)
            # 发送请求
            self.s.send(msg.encode())
            # 等待回复
            data=self.s.recv(128).decode()
            if data=="ok":
                global user_name
                user_name=name
                print("注册成功")
                home_main(self.s,name)
            else:
                print(data)
            return

    # 处理一级页面登录请求
    def do_log(self):
        while True:
            name=input("姓名:")
            password=getpass.getpass("密码:")
            if (" " in name) or (" " in password):
                print("用户名密码不能有空格")
                continue
            msg="L %s %s"%(name,password)
            # 发送请求
            self.s.send(msg.encode())
            # 等待回复
            data=self.s.recv(128).decode()
            if data=="ok":
                global user_name
                user_name = name
                print("登录成功")
                home_main(self.s,name)
            else:
                print(data)
            return

    # 处理一级页面退出请求
    def do_quit(self):
        self.s.send(b"Q")
        sys.exit("谢谢使用!")


# 处理二级页面--处理查词,记录
def home_main(s,name):
    operate_main=OperateMain(s,name)
    while True:
        print("""
================Query====================
--1.更改用户名      2.修改密码         3.注销--""")
        cmd=input("输入选项:")
        if cmd not in ["1","2","3"]:
            print("请输入正确选项")
            continue
        elif cmd=="1":
            operate_main.modify_name()
        elif cmd=="2":
            operate_main.modify_password()
        elif cmd=="3":
            msg="O %s"%user_name
            s.send(msg.encode())
            return

#　二级页面请求类
class OperateMain:
    """
        客户端二级页面请求类
    """
    def __init__(self,s,name):
        self.s=s
        self.name=name

    # 更改用户名请求
    def modify_name(self):
        msg="N %s"%self.name
        self.s.send(msg.encode())
        result=self.s.recv(128).decode()
        if result!="ok":
            print(result)
            return
        while True:
            mf_name=input("请输入更新的用户名：")
            if " " in mf_name:
                print("用户名不能有空格")
                continue
            self.s.send(mf_name.encode())
            r=self.s.recv(128).decode()
            if r=="ok":
                self.name=mf_name
                print("修改成功")
                break
            print(r)


    # 更改密码请求
    def modify_password(self):
        msg = "P %s" % self.name
        self.s.send(msg.encode())
        result = self.s.recv(128).decode()
        if result != "ok":
            print(result)
            return
        while True:
            mf_password = input("请输入更新的密码：")
            if " " in mf_password:
                print("密码不能有空格")
                continue
            self.s.send(mf_password.encode())
            r = self.s.recv(128).decode()
            if r == "ok":
                print("修改成功")
                break
            print(r)




if __name__=="__main__":
    try:
        main()
    except Exception:
        sql = "update users set status=0 where name='%s'" %user_name
        db_helper.DBConnector().do_update(sql)









