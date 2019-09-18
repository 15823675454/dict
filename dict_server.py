from socket import *
from threading import *
from multiprocessing import process
import pymysql
import os,sys
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)


class DictServer(Thread):
    def __init__(self, c, addr):
        super().__init__()
        self.c = c
        self.addr = addr
        self.db = pymysql.connect(user='root',
                                  passwd='123456',
                                  database='dict',
                                  charset='utf8')
        self.cur = self.db.cursor()


    def register(self, name):
        sql = 'select * from user where name=%s'
        self.cur.execute(sql, [name])
        data = self.cur.fetchone()
        if data:
            self.c.send('该用户已存在！'.encode())
        else:
            self.c.send('OK'.encode())
            passwd = self.c.recv(1024).decode()
            sql = 'insert into user values(%s,%s)'
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            self.c.send('OK'.encode())

    def login(self, name):
        sql = 'select * from user where name=%s'
        self.cur.execute(sql, [name])
        data = self.cur.fetchone()
        if data:
            self.c.send(b'OK')
            data = self.c.recv(1024).decode()
            sql = 'select * from user where name=%s and passwd=%s'
            self.cur.execute(sql, [name, data])
            data = self.cur.fetchone()
            if data:
                self.c.send(b'OK')
                self.dict_word()
            else:
                self.c.send('密码错误'.encode())
        else:
            self.c.send('该用户名不存在'.encode())
    def run(self):
        while True:
            data = self.c.recv(1024).decode()
            if not data or data == 'Q':
                return
            list1 = data.split(' ')
            if list1[0] == 'R':
                self.register(list1[1])
            elif list1[0] == 'L':
                self.login(list1[1])

    def dict_word(self):
        while True:
            data = self.c.recv(1024).decode()
            if data == 'q':
                self.c.send("EXIT".encode())
                break
            sql = 'select * from words where word=%s'
            self.cur.execute(sql, [data])
            mean = self.cur.fetchall()[0]
            print(mean)
            self.c.send(mean[2].encode())



def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    while True:
        c, addr = sockfd.accept()
        print('connect from', addr)
        t = DictServer(c, addr)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()




if __name__ == '__main__':
    pass







