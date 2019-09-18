from socket import *
import sys,os
from getpass import getpass
from time import ctime
ADDR = ('127.0.0.1', 8888)


def register(s):
    while True:
        print('+=========注册========+')
        name = input('请输入用户名：')
        if ' ' in name:
            print('用户名格式错误')
            continue
        msg = 'R '+name
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'OK':
            print('该用户名可用')
            passwd = getpass('请输入密码：')
            if not passwd:
                print('密码不能为空！')
                continue
            again = getpass('请确认密码：')
            if passwd == again:
                s.send(passwd.encode())
                data = s.recv(1024).decode()
                if data == 'OK':
                    print('注册成功，请登录')
                    break
                else:
                    print('注册失败,请重新注册')
                    continue
            else:
                continue
        else:
            print(data)


def select_2(name):
    print("+==========%s==========+" % name)
    print("+******  #1 查单词  ****+")
    print("+******  #2 注销    ****+")
    print("+******  #3 历史记录 ***+")
    print("+======================+")


def word(s):
    f = open('log.txt', 'ab+')
    while True:
        print('+******查单词********+')
        print('+******q退出********+')
        user = input('请输入您要查询的单词:').strip()
        s.send(user.encode())
        data = s.recv(1024).decode()
        if data == "EXIT":
            break
        print(data)
        msg = user + ' |' + data + ' |' + ctime() + '\n'
        f.write(msg.encode())

def history():
    try:
        f = open('log.txt', 'rb')
    except FileNotFoundError:
        print('历史记录为空')
        return
    # print(f)
    for line in f:
        print(line.decode())


def login_choise(name, s):
    while True:
        select_2(name)
        n = input('请输入：')
        if n == '1':
            word(s)
        elif n == '2':
            break
        elif n == '3':
            history()
        else:
            print('输入有误！')

def login(s):
    while True:
        name = input('请输入用户名：').strip()
        msg = 'L '+name
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'OK':
            passwd = getpass('请输入密码：').encode()
            s.send(passwd)
            data = s.recv(1024).decode()
            if data == 'OK':
                # 登陆成功
                login_choise(name, s)
                break
            else:
                print(data)
        else:
            print(data)


def select():
    print("+--------------菜单----------------+")
    print("+-----------1.注册输入R------------+")
    print("+-----------2.登录输入L------------+")
    print("+-----------3.退出输入Q------------+")
    print("+------------这是底线--------------+")
def main():
    sockfd = socket()
    sockfd.connect(ADDR)
    while True:
        try:
            select()
            userin = input("请输入：")
        except Exception as e:
            print(e)
            continue
        except KeyboardInterrupt:
            userin = 'Q'
        if userin == "R":
            register(sockfd)
        elif userin == "L":
            login(sockfd)
        elif userin == "Q":
            sockfd.send('Q'.encode())
            sys.exit("退出客户端")
        else:
            print('输入有误')
if __name__ == '__main__':
    main()



