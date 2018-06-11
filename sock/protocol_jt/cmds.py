#-*- coding:utf-8 -*-
import struct
from config import BYTE_ORDER

class BaseCMD:
    self.cmd = ''
    self.flag = 0
    self.tn = '\x00'
    self.sn = '1234567890123456'
    self.data = ''
    
    def do(self):
        pass
    
    def pkg(self):
        pass

    def unpack(self, data):
        pass

class CMD1(BaseCMD):
    self.cmd = '\x01'

    def do(self):
        print 'do cmd1'
        pass

    def pkg(self):
        self.flag = 0
        self.tn = '\x00'
        #self.data = struct.pack('c', 'a') + struct.pack(BYTE_ORDER + 'H', 12)

    def unpack(self, data):
        self.active_rst = struct.unpack('c', data[0])
        self.protocol_version = struct.unpack(BYTE_ORDER + 'H', data[1:3])
        print self.active_rst, self.protocol_version

class CMD2(BaseCMD):
    self.cmd = '\x02'
    
    def do(self):
        print 'do cmd2'
        pass

    def pkg(self):
        self.flag = 0
        self.tn = '\x00'

    def unpack(self, data):
        self.factory = struct.unpack(BYTE_ORDER + 'H', data[0:2])
        self.soft_version = struct.unpack(BYTE_ORDER + 'H', data[2:4])
        self.protocol_version = struct.unpack(BYTE_ORDER + 'H', data[4:6])
        self.max_vol = struct.unpack(BYTE_ORDER + 'I', data[6:10])
        self.min_vol = struct.unpack(BYTE_ORDER + 'I', data[10:14])
        self.max_dc = struct.unpack(BYTE_ORDER + 'I', data[14:18])
        self.power = struct.unpack(BYTE_ORDER + 'I', data[18:22])
        self.build_date = struct.unpack(BYTE_ORDER + 'I', data[22:26])
        self.dev_type = struct.unpack('c', data[26])
        self.gun_num = struct.unpack('c', data[27])
        self.dev_charge_type = struct.unpack('c', data[28])
