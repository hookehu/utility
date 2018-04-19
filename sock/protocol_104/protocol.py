#-*- coding:utf-8 -*-
import struct
from config import BYTE_ORDER
from cmds import *

def crc_1byte(data):
    crc_1byte = 0
    for i in range(0, 8):
        if ((crc_1byte ^ data) & 0x01):
            crc_1byte ^= 0x18
            crc_1byte >>= 1
            crc_1byte |= 0x80
        else:
            crc_1byte >>= 1
    return crc_1byte

def crc_byte(data):
    rst = 0
    for byte in data:
        byte = ord(byte)
        print byte
        rst = (crc_1byte(rst ^ byte))
    return rst
    
class APDU:
    apci = None
    asdus = []
    
class APCI:
    i = None
    u = None
    s = None
    
class I:
    send_sn = '' #little-endian len 2 byte
    recv_sn = '' #little-endian len 2 byte
    
class S:
    one = '\x01'
    two = '\x00'
    recv_sn = '' #little-endian len 2 byte
    
class U:
    flag = '' #test_con test_act stop_con stop_act start_con start_act 1 1
    two = '\x00'
    three = '\x00'
    four = '\x00'
print dir()
class BaseProtocol:
    cmds = {
    CMD1.cmd:CMD1,
    CMD2.cmd:CMD2,
    }

    def decode(self, stream):
        rst = self.do_decode(stream)
        return rst
        

    def do_decode(self, stream):
        print 'stream len', len(stream)
        head = struct.unpack('c', stream[0])[0]
        if head != '\xab':
            print 'none head', ord(head), ord('\xab'), head == '\xab'
            return False, None
        if len(stream) < 5:
            print 'no enough len'
            return False, None
        dlen = struct.unpack(BYTE_ORDER + 'I', stream[1:5])[0]
        if len(stream) < 5 + dlen:
            print 'no enough len for data', len(stream), dlen
            return False, None
        flag = struct.unpack(BYTE_ORDER + 'I', stream[5:9])[0]
        cmd = struct.unpack('c', stream[9])[0]
        sn = struct.unpack(BYTE_ORDER + '16s', stream[10:10+16])[0]
        tn = struct.unpack('c', stream[26])[0]
        tl = 4 + 1 + 16 + 1 + 1 #数据包长：flag + cmd + sn + type + data + crc
        print dlen, tl, sn
        dataend = 27 + dlen - tl
        if dlen > tl:
            data = struct.unpack(BYTE_ORDER + str(dlen -  tl) + 's', stream[27:dataend])[0]
        crc = struct.unpack('c', stream[dataend])[0]
        end = struct.unpack('c', stream[dataend + 1])[0]
        print 'decode end', ord(end), ord('\xed')
        c = self.cmds[cmd]()
        if dlen > tl:
            c.unpack(data)
        print 'jjjj'
        return True, c, stream[dataend + 1 + 1:]

    def encode(self, cmd_data):
        pkg = ''
        cmd = cmd_data.cmd
        flag = cmd_data.flag
        tn = cmd_data.tn
        sn = cmd_data.sn
        #pkg = pkg + struct.pack('c', 'x\ab') #head
        data = cmd_data.data
        datalen = len(cmd_data.data)
        dlen = 4 + 1 + 16 + 1 + datalen + 1
        pkg = pkg + struct.pack(BYTE_ORDER + 'I', dlen) #len
        pkg = pkg + struct.pack(BYTE_ORDER + 'I', flag) #flag
        pkg = pkg + struct.pack('c', cmd) #cmd
        pkg = pkg + struct.pack(BYTE_ORDER + '16s', sn) #SN
        pkg = pkg + struct.pack('c', tn) #type or num
        if datalen > 0:
            pkg = pkg + struct.pack(BYTE_ORDER + str(datalen) + 's', data) #data
        crc = crc_byte(pkg)
        print 'crc', crc
        crc = chr(crc)
        pkg = pkg + struct.pack('c', crc) #crc
        pkg = pkg + struct.pack('c', '\xed') #end
        pkg = struct.pack('c', '\xab') + pkg #head
        return pkg

