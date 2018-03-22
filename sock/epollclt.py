#-*- coding:utf-8 -*-
import struct
import select
import socket
from epollsvr import Channel
from protocol import *
from config import CLT_HOST, CLT_PORT

class Client:

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((CLT_HOST, CLT_PORT))
        self.timeout = 1
        self.epoll = select.epoll()
        self.epoll.register(sock.fileno(), select.EPOLLIN)
        self.sock = sock
        self.channel = Channel(sock, self.epoll)

    def run(self):
        cmd = '1'
        while True:
            events = self.epoll.poll(self.timeout)
            print cmd
            if not events:
                print cmd
                if cmd == '1':
                    print '1'
                    p = struct.pack('!i2si', 1, 'ab', 34)
                    print p
                    #self.channel.write(p)
                    self.cmd1()
                    cmd = '2'
                elif cmd == '2':
                    print '2'
                    pp = struct.pack('<i2si', 2, 'bc', 34)
                    print len(pp)
                    #self.channel.write(pp)
                    cmd = 'exit'
                elif cmd == 'exit':
                    break
                continue
            for fd, event in events:
                if event & select.EPOLLHUP:
                    self.epoll.unregister(self.sock.fileno())
                    self.channel.close()
                elif event & select.EPOLLIN:
                    self.channel.read()
                    self.epoll.modify(self.sock.fileno(), select.EPOLLIN)
                elif event & select.EPOLLOUT:
                    self.channel.real_send()
                    self.epoll.modify(self.sock.fileno(), select.EPOLLIN)

    def cmd1(self):
        pkg = CMD1().pkg()
	pkg = BaseProtocol().encode(pkg)
        self.channel.write(pkg)
	

if __name__ == "__main__":
    clt = Client()
    clt.run()
    
