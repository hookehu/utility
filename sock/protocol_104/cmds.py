#-*- coding:utf-8 -*-
import struct
from config import BYTE_ORDER

class BaseCMD:
    def __init__(self):
        pass
    
    def do(self):
        pass
    
    def pkg(self):
        pass

    def unpack(self, data):
        pass

    def decode_bcd(self, value):
        tmp = []
        i = 0
        vlen = len(value)
        while i < vlen:
            v = struct.unpack('B', value[i])
            h = Byte(v) >> 4
            t = Byte(v) << 4
            l = Byte(t) >> 4
            tmp.append(str(h))
            tmp.append(str(l))
            i = i + 1
        rst = 0
        _len = len(tmp)
        s = ''.join(tmp)
        return int(s)


    def encode_bcd(self, value):
        tmp = str(value)
        i = 0
        rst = ''
        _len = len(tmp) * 0.5
        while i < _len:
            h = int(tmp[i * 2])
            l = int(tmp[i * 2 + 1])
            v = h << 4 & l
            rst = rst + struct.pack('B', v)
        return rst
