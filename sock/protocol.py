#-*- coding:utf-8 -*-
import struct
from config import BYTE_ORDER

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

class BaseProtocol:

    def decode(self, stream):
        rst = self.do_decode(stream)
        if not rst[0]:
            return rst
        

    def do_decode(self, stream):
        print 'stream len', len(stream)
        head = struct.unpack('c', stream[0])[0]
        if head != '\xab':
            print 'none head', ord(head), ord('\xab'), head == '\xab'
            return False, None
        dlen = struct.unpack(BYTE_ORDER + 'I', stream[1:5])[0]
        flag = struct.unpack(BYTE_ORDER + 'I', stream[5:9])[0]
        cmd = struct.unpack('c', stream[9])[0]
        sn = struct.unpack(BYTE_ORDER + '16s', stream[10:10+16])[0]
        tn = struct.unpack('c', stream[26])[0]
        tl = 4 + 1 + 16 + 1 + 1 #数据包长：flag + cmd + sn + type + data + crc
        print dlen, tl, sn
        dataend = 27 + dlen - tl
        if dlen > tl:
            self.data = struct.unpack(BYTE_ORDER + str(dlen -  tl) + 's', stream[27:dataend])[0]
        crc = struct.unpack('c', stream[dataend])[0]
        end = struct.unpack('c', stream[dataend + 1])[0]
        print 'decode end', ord(end), ord('\xed')
        return True, stream[dataend + 1 + 1:]

    def encode(self, cmd_data):
        pkg = ''
        cmd = '\x00'
        flag = 0
        tn = '\x00'
        sn = '1234567890123456'
        #pkg = pkg + struct.pack('c', 'x\ab') #head
        data = '\x01'
        datalen = 1
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

class BaseCMD:
    
    def do(self):
        pass
    
    def pkg(self):
        pass

    def unpack(self, data):
        pass

class CMD1(BaseCMD):
    cmd = '\x01'

    def do(self):
        pass

    def pkg(self):
        pass

    def unpack(self, data):
        active_rst = struct.unpack('c', data[0])
        protocol_version = struct.unpack(BYTE_ORDER + 'H', data[1:3])

class CMD2(BaseCMD):
    cmd = '\x02'
    
    def do(self):
        pass

    def pkg(self):
        pass

    def unpack(self, data):
        factory = struct.unpack(BYTE_ORDER + 'H', data[0:2])
        soft_version = struct.unpack(BYTE_ORDER + 'H', data[2:4])
        protocol_version = struct.unpack(BYTE_ORDER + 'H', data[4:6])
        max_vol = struct.unpack(BYTE_ORDER + 'I', data[6:10])
        min_vol = struct.unpack(BYTE_ORDER + 'I', data[10:14])
        max_dc = struct.unpack(BYTE_ORDER + 'I', data[14:18])
        power = struct.unpack(BYTE_ORDER + 'I', data[18:22])
        build_date = struct.unpack(BYTE_ORDER + 'I', data[22:26])
        dev_type = struct.unpack('c', data[26])
        gun_num = struct.unpack('c', data[27])
        dev_charge_type = struct.unpack('c', data[28])
