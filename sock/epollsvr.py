#-*- coding:utf-8 -*_
import select
import socket
import struct
from protocol import *
from config import SVR_HOST, SVR_PORT

class Channel:
    def __init__(self, fd, epoll):
        self.pkgs = []
        self.sock = fd
        self.epoll = epoll

    def read(self):
        data = self.sock.recv(1024)
        if data:
           print 'data', data, len(data)
           for k in data:
               print 'k', struct.unpack('c', k)
           CMD1().decode(data)

    def write(self, pkg):
        self.pkgs.append(pkg)
        self.epoll.modify(self.sock.fileno(), select.EPOLLOUT)


    def real_send(self):
        for pkg in self.pkgs:
            self.sock.send(pkg)

    def close(self):
        self.sock.close()

class Server:
    def __init__(self):
        self.channels = {}
        pass

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(SVR_HOST, SVR_PORT))
        sock.listen(2048)
        sock.setblocking(False)
        timeout = 1
        self.epoll = select.epoll()
        self.epoll.register(sock.fileno(), select.EPOLLIN)
        self.sock_fd = sock.fileno()
        while True:
            events = self.epoll.poll()
            if not events:
                continue
            for fd, event in events:
                if fd == self.sock_fd:
                    conn, addr = sock.accept()
                    conn.setblocking(False)
                    channel = Channel(conn, self.epoll)
                    self.epoll.register(conn.fileno(), select.EPOLLIN)
                    self.channels[conn.fileno()] = channel
                elif event & select.EPOLLHUP:
                    self.epoll.unregister(fd)
                    self.channels[fd].close()
                    del self.channels[fd]
                elif event & select.EPOLLIN:
                    self.channels[fd].read()
                    self.epoll.modify(fd, select.EPOLLIN)
                elif event & select.EPOLLOUT:
                    self.channels[fd].real_send()
                    self.epoll.modify(fd, select.EPOLLIN)

        

if __name__ == "__main__":
    svr = Server()
    svr.run()
