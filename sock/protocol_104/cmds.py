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
        return decode_bcd(value)


    def encode_bcd(self, value):
        return encode_bcd(value)
