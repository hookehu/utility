#-*- coding:utf-8 -*-
import struct
from config import BYTE_ORDER
from cmds import *

#104规约是小端字节序

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

class ASDUTYPE:
    '''
    5.4.2.1 类型标识

    在监视方向上的过程信息
    类型标识 = TYPE IDENTIFICATION:=UI8[1...8] 
    <1> := 不带时标的单点信息 M_SP_NA_1
    <11> := 测量值，标度化值, 长度小于等于 2 字节 M_ME_NA_1
    <15> := 累积量(不带时标) M_IT_NA_1
    <130> := 充电桩消费记录数据 M_RE_NA_1
    <131> := 分箱式充电机计量数据 M_CM_NA_1
    <132> := 测量值，标度化值，长度大于 2 字节 M_MD_NA_1
    <133> := 下发数据项 M_SD_NA_1
    <134> := 监测数据项 M_JC_NA_1

    在控制方向上的过程信息
    类型标识 = TYPE IDENTIFICATION:=UI8[1...8] 
    <100> := 总召唤命令 C_IC_NA_1
    <101> := 计数量总召命令 C_CI_NA_1
    <103> := 时钟同步命令 C_CS_NA_1
    <105> := 重启命令 C_RP_NA_1
    <106> := 故障告警上传命令 C_CD_NA_1
    <113> := 参数设置命令 P_AC_NA_1
    <114> := 预约参数配置 P_AB_NA_1
    <115> := 蓝牙参数配置 P_AF_NA_1 
    <116> := 地锁参数配置 P_AD_NA_1 
    <117> := 软件升级命令 P_AE_NA_1 
    <118> := 工作状态切换命令 P_WS_NA_1
    '''
    M_SP_NA_1 = 1
    M_ME_NA_1 = 11
    M_IT_NA_1 = 15
    M_RE_NA_1 = 130
    M_CM_NA_1 = 131
    M_MD_NA_1 = 132
    M_SD_NA_1 = 133
    M_JC_NA_1 = 134
    C_IC_NA_1 = 100
    C_CI_NA_1 = 101
    C_CS_NA_1 = 103
    C_RP_NA_1 = 105
    C_CD_NA_1 = 106
    P_AC_NA_1 = 113
    P_AB_NA_1 = 114
    P_AF_NA_1 = 115
    P_AD_NA_1 = 116
    P_AE_NA_1 = 117
    P_WS_NA_1 = 118

class CAUSETYPE:
    '''
    5.4.2.4 传送原因

    原因 = Cause := CP8[1...8]<0...255>
    <0> := 未用
    <1> := 周期、循环
    <2> := 背景扫􏰁 back 
    <3> := 突发(自发) spont 
    <4> := 初始化 init 
    <5> := 请求或被请求 req 
    <6> := 激活
    <7> := 激活确认
    <8> : = APP激活充电
    <9> : = APP 激活充电确认
    <20> := 响应站总召
    <21>:=响应第 1 组召唤 
    <22>:=响应第 2 组召唤
    至
    <36>:=响应第 16 组召唤
    <44> := 未知的类型标识
    <45> := 未知的传送原因
    <46> := 未知的应用服务数据单元公共地址 
    <47> := 未知的信息对象地址
    '''
    not_use = 0
    cyc = 1
    back = 2
    spont = 3
    init = 4
    req = 5
    active = 6
    active_con = 7
    app_active = 8
    app_active_con = 9
    introegen = 20
    unknow_type = 44
    unknow_cause = 45
    unknow_asdu_common_addr = 46
    unknow_info_addr = 47

class CP56Time(BaseCMD):
    def __init__(self):
        self.ms = 0
        self.minute = 0
        self.clock = 0
        self.day = 0
        self.month = 0
        self.year = 0

    def unpack(self, data):
        self.ms = struct.unpack(BYTE_ORDER + 'H', data[0:2])[0]
        self.minute = struct.unpack('B', data[2])[0]
        self.clock = struct.unpack('B', data[3])[0]
        self.day = struct.unpack('B', data[4])[0]
        self.month = struct.unpack('B', data[5])[0]
        self.year = struct.unpack('B', data[6])[0]
        return data[7:]

    def pkg(self):
        d = ''
        d = d + struct.pack('H', self.ms)
        d = d + struct.pack('B', self.minute)
        d = d + struct.pack('B', self.clock)
        d = d + struct.pack('B', self.day)
        d = d + struct.pack('B', self.month)
        d = d + struct.pack('B', self.year)
        self.data = d

class SIQ(BaseCMD):
    '''
    5.4.2.8 带品质􏰁述词的单点信息(IEV 371-02-07)

    SIQ:=CP8{SPI，RES，BL，SB，NT，IV} 
    SPI=单点信息:=BS1[1]<0..1> (TYPE 6) 
    <0>:=开
    <1>:=合
    RES=RESERVE:=BS3[2..4]<0> (TYPE 6) 
    BL:=BS1[5]<0..1> (TYPE 6) 
    <0>:=未被封锁 
    <1>:=被封锁 
    SB:=BS1[6]<0..1> (TYPE 6) 
    <0>:=未被取代 
    <1>:=被取代 
    NT:=BS1[7]<0..1> (TYPE 6) 
    <0>:=当前值 
    <1>:=非当前值 
    IV:=BS1[8]<0..1> (TYPE 6) 
    <0>:=有效
    <1>:=无效
    '''
    def __init__(self):
        BaseCMD.__init__(self)
        self.SPI = 0
        self.RES = 0
        self.BL = 0
        self.SB = 0
        self.NT = 0
        self.IV = 0

    def unpack(self, data):
        v = struct.unpack('B', data[0])[0]
        self.SPI = v & 1
        self.RES = (v >> 1) & 7
        self.BL = (v >> 4) & 1
        self.SB = (v >> 5) & 1
        self.NT = (v >> 6) & 1
        self.IV = (v >> 7) & 1
        #return data[1:]

    def pkg(self):
        v = (self.IV << 7) + (self.NT << 6) + (self.SB << 5) + (self.BL << 4) + (self.RES << 1) + self.SPI
        self.data = struct.pack('B', v)


class SVA(BaseCMD):
    '''
    5.4.2.9 标度化值(SVA)

    SVA:=F16[1..16]<-215..+215-1>
    没有定义测量值的分辩率，如果测量值的分辩率比 LSB 的最小单位粗，则这些 LSB 位设置为零。
    '''
    def __init__(self):
        BaseCMD.__init__(self)
        self.SVA = 0

    def unpack(self, data):
        self.SVA = struct.unpack(BYTE_ORDER + 'h', data[0:2])[0]
        #return data[2:]

    def pkg(self):
        self.data = struct.pack(BYTE_ORDER + 'h', self.SVA)

class QDS(BaseCMD):
    '''
    5.4.2.10品质􏰁述词(单个八位位组)

    QDS:=CP8{OV，RES，BL，SB，NT，IV}
    OV:=BS1[1] <0..1> (TYPE 6)
    <0>:=未溢出
    <1>:=溢出
    RES=RESERVE:=BS3[2..4] (TYPE 6)
    <0> 
    BL:=BS1[5]<0..1> (TYPE 6) 
    <0>:=未被封锁
    <1>:=被封锁 
    SB:=BS1[6]<0..1> (TYPE 6) 
    <0>:=未被取代
    <1>:=被取代 
    NT:=BS1[7]<0..1> (TYPE 6) 
    <0>:=当前值
    <1>:=非当前值 
    IV:=BS1[8]<0..1> (TYPE 6) 
    <0>:=有效
    <1>:=无效
    OV=溢出/未溢出 
    信息对象的值超出了预先定义值的范围(主要适用模拟量值) 
    BL=被封锁/未被封锁 
    信息对象的值为传输而被封锁，值保持封锁前被采集的状态。封锁和解锁可以由当地联锁机构或当地自动原因启动。
    SB=被取代/未被取代 
    信息对象的值由值班员(调度员)输入或者由当地自动原因所􏰀供。 
    NT=当前值/非当前值 
    若最近的刷新成功则值就称为当前值，若一个指定的时间间隔内刷新不成功或者其值不可用,值就称为非当前值。 
    IV=有效/无效
    若值被正确采集就是有效，在采集功能确认信息源的反常状态(丧失或非工 作刷新装置)则值就是无效。信息对象的值在这些条件下没有被定义。标上无效用以􏰀醒使用者，此值不正确而不能使用
    '''
    def __init__(self):
        BaseCMD.__init__(self)
        self.OV = 0
        self.RES = 0
        self.BL = 0
        self.SB = 0
        self.NT = 0
        self.IV = 0

    def unpack(self, data):
        v = struct.unpack('B', data[0])[0]
        self.OV = v & 1
        self.RES = (v >> 1) & 7
        self.BL = (v >> 4) & 1
        self.SB = (v >> 5) & 1
        self.NT = (v >> 6) & 1
        self.IV = (v >> 7) & 1
        #return data[1:]

    def pkg(self):
        v = (self.IV << 7) + (self.NT << 6) + (self.SB << 5) + (self.BL << 4) + (self.RES << 1) + self.OV
        self.data = struct.pack('B', v)

class BCR(BaseCMD):
    '''
    5.4.2.11二进计数量读数(BCR)

    BCR:=CP40{Counter reading,Sequence notation}
    Counter reading =计数量读数:=I32[1..32]<-231..+231-1> (Type 2.1) 
    Sequence notation=顺序记法:=CP8{SQ,CY,CA,IV} 
    SQ=顺序号:=UI5[33..37]<0..31> (Type 1.1)
    CY=进位:=BS1[38]<0..1> (TYPE 6)
    <0>:=在相应的累加周期内未溢出
    <1>:=在相应的累加周期内溢出 
    CA=计数量被调整:=BS1[39]<0..1> (TYPE 6) 
    <0>:=上次读数后计数量未被调整
    <1>:=上次读数后计数量被调整
    IV=无效:=BS1[8]<0..1> (TYPE 6)
    <0>:=有效
    <1>:=无效
    SQ=顺序号
    CY=进位
    CA=计数量被调整
    '''
    def __init__(self):
        BaseCMD.__init__(self)
        self.COUNTER = 0
        self.SQ = 0
        self.CY = 0
        self.CA = 0
        self.IV = 0

    def unpack(self, data):
        counter = struct.unpack(BYTE_ORDER + 'I', data[0:4])[0]
        self.COUNTER = counter
        v = struct.unpack('B', data[4])[0]
        self.SQ = v & 31
        self.CY = (v >> 5) & 1
        self.CA = (v >> 6) & 1
        self.IV = v >> 7
        #return data[5:]

    def pkg(self):
        d = ''
        d = struct.pack(BYTE_ORDER + 'I', self.COUNTER)
        v = (self.IV << 7) + (self.CA << 6) + (self.CY << 5) + self.SQ
        d = d + struct.pack('B', v)
        self.data = d

class QOI(BaseCMD):
    '''
    5.4.2.12召唤限定词

    改变当地参数后的初始化(QOI) (TYPE 1.1) 
    QOI:=UI[1..8\<0..255>
    <0>:=未用 
    <1..19>:=为本配套标准的标准定义保留(兼容范围) 
    <20>:=响应站召唤
    '''
    def __init__(self):
        BaseCMD.__init__(self)
        self.QOI = 0

    def unpack(self, data):
        v = struct.unpack('B', data[0])[0]
        self.QOI = v
        #return data[1:]

    def pkg(self):
        self.data = struct.pack('B', self.QOI)

class QCC(BaseCMD):
    '''
    5.4.2.13计数量召唤命令限定词(QCC)

    QCC:=CP8{RQT,FRZ} 
    RQT=请求:=UI6[1..6]<0..63> (TYPE 1.1) 
    <0>:=无请求计数量(未采用)
    <1>:=请求计数量第 1 组
    <5>:=总的请求计数量 
    <6..31>:=为本配套标准的标准定义保留(兼容范围) 
    <32..63>:=为特定使用保留 
    FRZ=冻结:=UI2[7..8]<0..63>
    <0>:=读(无冻结和复位) 
    <1>:=计数量冻结不带复位(被冻结的值代表增量信息) 
    <2>:=计数量冻结带复位
    <3>:=计数量复位
    由 FRZ 码所规定的动作仅用于由 RQT 码所规定的组。
    '''
    def __init__(self):
        BaseCMD.__init__(self)
        self.RQT = 0
        self.FRZ = 0

    def unpack(self, data):
        v = struct.unpack('B', data[0])[0]
        self.RQT = v & 63
        self.FRZ = (v >> 6) & 3
        #return data[1:]

    def pkg(self):
        v = (self.FRZ << 6) + self.RQT
        self.data = struct.pack('B', v)
    
class APDU(BaseCMD):

    def __init__(self):
        BaseCMD.__init__(self)
        self.start_flag = 0
        self.apdu_len = 0 #max length 253
        self.apci = None
        self.asdu = None

    def unpack(self, data):
        self.start_flag = struct.unpack('B', data[0:1])[0]
        self.apdu_len = struct.unpack('B', data[1:2])[0]
        self.apci = APCI()
        data = self.apci.unpack(data[2:])
        asdu_type = struct.unpack('B', data[0])[0]
        if asdu_type == ASDUTYPE:
            self.asdu = M_SP_NA_1()
            self.asdu.unpack(data)
        print('asdu type', asdu_type)

    def pkg(self):
        pkg = ''
        pkg = pkg + struct.pack('B', self.start_flag)
        print('pkg', pkg)
        d = ''
        if self.apci is not None:
            self.apci.pkg()
            d = d + self.apci.data
            print('d', d)
        if self.asdu is not None:
            self.asdu.pkg()
            d = d + self.asdu.data
            print('f', self.asdu.data)
        _l = len(d)
        _l = _l + 2
        self.apdu_len = _l
        pkg = pkg + struct.pack('B', self.apdu_len)
        pkg = pkg + d
        self.data = pkg
    
class APCI(BaseCMD):
    
    def __init__(self):
        BaseCMD.__init__(self)
        self.i = None
        self.u = None
        self.s = None

    def unpack(self, data):
        one = struct.unpack('B', data[0])[0]
        two = struct.unpack('B', data[1])[0]
        three = struct.unpack('B', data[2])[0]
        four = struct.unpack('B', data[3])[0]
        if one & 0x01 == 1:
            if one & 2 == 0:
                #S
                self.s = S()
                self.s.recv_sn = four << 7 + three >> 1
            else:
                #U
                self.u = U()
                self.u.flag = one
                self.u.test_c = one & (1 << 7)
                self.u.test_v = one & (1 << 6)
                self.u.stop_c = one & (1 << 5)
                self.u.stop_v = one & (1 << 4)
                self.u.start_c = one & (1 << 3)
                self.u.start_v = one & (1 << 2)
        else:
            #I
            self.i = I()
            self.i.send_sn = two << 7 + one >> 1
            self.i.recv_sn = four << 7 + three >> 1
        return data[4:]

    def pkg(self):
        if self.i is not None:
            self.i.pkg()
            self.data = self.i.data
        if self.u is not None:
            self.u.pkg()
            self.data = self.u.data
        if self.s is not None:
            self.s.pkg()
            self.data = self.s.data

    
class I(BaseCMD):#for has sid common info
    def __init__(self):
        BaseCMD.__init__(self)
        self.send_sn = 0 #little-endian len 2 byte
        self.recv_sn = 0 #little-endian len 2 byte

    def pkg(self):
        self.data = struct.pack(BYTE_ORDER + 'H', self.send_sn)
        self.data = self.data + struct.pack(BYTE_ORDER + 'H', self.recv_sn)
    
class S(BaseCMD):#for watch info
    def __init__(self):
        BaseCMD.__init__(self)
        self.one = 1
        self.two = 0
        self.recv_sn = 0 #little-endian len 2 byte

    def pkg(self):
        self.data = struct.pack('B', self.one)
        self.data = self.data + struct.pack('B', self.two)
        self.data = self.data + struct.pack(BYTE_ORDER + 'H', self.recv_sn)
    
class U(BaseCMD):#for other control info no sid
    def __init__(self):
        BaseCMD.__init__(self)
        self.test_c = 0
        self.test_v = 0
        self.start_c = 0
        self.start_v = 0
        self.stop_c = 0
        self.stop_v = 0
        self.flag = 3 #test_con test_act stop_con stop_act start_con start_act 1 1
        self.two = '\x00'
        self.three = '\x00'
        self.four = '\x00'

    def pkg(self):
        one = self.test_c << 7 + self.test_v << 6 + self.stop_c << 5 + self.stop_v << 4 + self.start_c << 3 + self.start_v << 2 + 1 << 1 + 1
        self.data = self.data + struct.pack('B', one) + self.two + self.three + self.four

class ASDU(BaseCMD):
    def __init__(self):
        BaseCMD.__init__(self)
        self.asdu_type = 0 #len 1 byte
        self.var_struct = 0 #len 1 byte for meta info count range 0-127 [1..7]  [8] is SQ
        self.cause = 0  #len 2 byte [1..8]
        self.common_addr = 0 #len 2 byte  0:not use  65535:global_addr  1-65534:stage_addr
        self.SQ = 0
        self.info_num = 0
        self.info_addrs = []
        self.infos = []

    def get_info_addr(self, data):
        ia0 = struct.unpack(BYTE_ORDER + 'B', data[0])[0]
        ia1 = struct.unpack(BYTE_ORDER + 'B', data[1])[0]
        ia2 = struct.unpack(BYTE_ORDER + 'B', data[2])[0]
        ia = ia0 << 16 + ia1 << 8 + ia2
        return ia

    def info_addr_todata(self, value):
        d = ''
        ia0 = value >> 16
        ia1 = value >> 8 - ia0 << 8
        ia2 = value - ia0 << 16 - ia1 << 8
        d = struct.pack('B', ia0)
        d = d + struct.pack('B', ia1)
        d = d + struct.pack('B', ia2)
        return d

    def do(self):
        print("not implement")
        pass
    
    def pkg(self):
        self.data = ''

    def unpack(self, data):
        self.asdu_type = struct.unpack('B', data[0])[0]
        self.var_struct = struct.unpack('B', data[1])[0]
        self.cause = struct.unpack(BYTE_ORDER + 'H', data[2:4])[0]
        self.common_addr = struct.unpack(BYTE_ORDER + 'H', data[4:6])[0]
        self.SQ = self.var_struct & 128
        self.info_num = self.var_struct & 127
        self.cause = self.cause
        return data[6:]

class M_SP_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def do(self):
        print("M_SP_NA_1 do");

    def pkg(self):
        ASDU.pkg(self)
        self.data = self.data + struct.pack('B', self.asdu_type)
        vs = self.SQ << 7 + self.info_num
        self.data = self.data + struct.pack('B', vs)
        self.data = self.data + struct.pack('B', self.cause)
        self.data = self.data + struct.pack('B', self.common_addr)
        if self.SQ == 1:
            i = 0
            self.data = self.data + self.info_addr_todata(self.info_addrs[0])
            while i < self.info_num:
                self.infos[i].pkg()
                self.data = self.data + self.infos[i].data
                i = i + 1
        else:
            i = 0
            while i < self.info_num:
                self.data = self.data + self.info_addr_todata(self.info_addrs[i])
                self.infos[i].pkg()
                self.data = self.data + self.infos[i].data
                i = i + 1

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)   
        pass

    def unpack_sq1(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 1
        end = 3
        while i < self.info_num:
            siq = SIQ()
            siq.unpack(data[3 + i * step])
            #info = struct.unpack('B', data[3 + i * step])[0]
            self.infos.append(siq)
            end = 4 + i * step
            i = i + 1
        return data[end:]

    def unpack_sq0(self, data):
        i = 0
        step = 4
        end = 0
        while i < self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            #info = struct.unpack('B', data[3 + i * step])[0]
            siq = SIQ()
            siq.unpack(data[3 + i * step])
            end = 4 + i * step
            self.info.append(siq)
            i = i + 1
        return data[end:]

class M_ME_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq1(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 3
        end = 3
        while i <= self.info_num:
            value = struct.unpack(BYTE_ORDER + 'H', data[3 + i * step : 5 + i * step])
            qds = QDS()
            qds.unpack(data[5 + i * step])
            end = 6 + i * step
            self.infos.append(qds)
            i = i + 1
        return data[end:]

    def unpack_sq0(self, data):
        i = 0
        step = 6
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = struct.unpack(BYTE_ORDER + 'H', data[3 + i * step : 5 + i * step])
            qds = QDS()
            qds.unpack(data[5 + i * step])
            end = 6 + i * step
            self.infos.append(qds)
            i = i + 1
        return data[end:]

class M_IT_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq1(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 5
        end = 3
        while i <= self.info_num:
            bcr = BCR()
            bcr.unpack(data[3 + i * step : 8 + i * step])
            end = 8 + i * step
            self.infos.append(bcr)
            i = i + 1
        return data[end:]

    def unpack_sq0(self, data):
        i = 0
        step = 8
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            bcr = BCR()
            bcr.unpack(data[3 + i * step : 8 + i * step])
            end = 8 + i * step
            self.infos.append(bcr)
            i = i + 1
        return data[end:]

class M_RE_NA_1(ASDU):#unparse
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("M_RE_NA_1 unpack error SQ == 1")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1> :=鉴权数据包
            d = JQSJ()
            rst = d.unpack(data[1:])
            pass
        elif t == 2:
            #<2> :=在线情况下停止充电时上传记录数据
            d = TZCDSJ()
            rst = d.unpack(data[1:])
            pass
        elif t == 3:
            #<3> :=离线交易上线后上传交易记录数据
            d = SCJYSJ()
            rst = d.unpack(data[1:])
        return rst

class M_CM_NA_1(ASDU):#unparse

    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("M_CM_NA_1 unpack error SQ == 1")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1> :=分箱式充电机计量数据
            pass
        elif t == 2:
            #<2> :=换电机器人统计数据
            pass
        elif t == 3:
            #<3> :=充电架统计数据
            pass
        elif t == 4:
            #<4> :=在线换电机器换电业务计量数据
            pass
        elif t == 5:
            #<5> :=电池箱统计数据
            pass
        elif t == 6:
            #<6> :=鉴权数据包
            d = JQSJ()
            rst = d.unpack(data[1:])
        elif t == 7:
            #<7> :=车辆地理信息数据
            pass
        elif t == 8:
            #<8> :=车辆电池箱数据
            pass
        elif t == 9:
            #<9> :=电池箱实时监测数据
            pass
        return rst

class M_MD_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq1(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        offset = 3
        while i <= self.info_num:
            vlen = struct.unpack('B', data[offset])[0]
            value = data[offset + 1 : offset + 1 + vlen]
            info = struct.unpack('B', data[offset + 1 + vlen])[0]
            offset = offset + 1 + vlen + 1
            self.infos.append(info)
            i = i + 1
        return data[offset:]

    def unpack_sq0(self, data):
        offset = 0
        i = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[offset : offset + 3])
            self.info_addrs.append(ia)
            vlen = struct.unpack('B', data[offset + 3])[0]
            value = data[offset + 4 : offset + 4 + vlen]
            info = struct.unpack(BYTE_ORDER + 'B', data[offset + 4 + vlen])[0]
            offset = offset + 4 + vlen + 1
            self.infos.append(info)
            i = i + 1
        return data[offset:]

class M_SD_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("M_SD_NA_1 unpack error SQ == 1")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1> :=黑名单下发时下行数据
            d = HMDXFSJ()
            rst = d.unpack(data[1:])
        elif t == 2:
            #<2> :=下发标准费率
            d = XFBZFLSJ()
            rst = d.unpack(data[1:])
        elif t == 3:
            #<3> :=充电鉴权下行数据
            pass
        elif t == 4:
            #<4> :=充电扣款后下行数据
            pass
        elif t == 5:
            #<5> :=换电鉴权下行数据
            pass
        elif t == 6:
            #<6> :=换电扣款后下行数据
            pass
        elif t == 7:
            #<7> :=车载终端下行数据
            pass
        return rst

class M_JC_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("M_JC_NA_1 unpack error SQ == 1")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1> :=离散充电过程实时监测数据
            d = CDSCSJ()
            rst = d.unpack(data[1:])
        elif t == 2:
            #<2> := app 充电电桩上行数据
            pass
        return rst

#5.4.4在控制方向过程信息的应用服务数据单元
class C_IC_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        self.info_addrs.append(0)
        qoi = QOI()
        qoi.unpack(data)
        return data[1:]

class C_CI_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        self.info_addrs.append(0)
        qcc = QCC()
        qcc.unpack(data)
        return data[1:]

class C_CS_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        t = CP56Time()
        t.unpack(data)
        return data[7:]

class C_RP_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        self.info_addrs.append(0)
        return data[1:]

class C_CD_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        t = struct.unpack('B', data[0])[0]
        if t == 0:
            #0: 电桩主动上送信息， 数据定义见附表 5.7.26 表 5-53 中心收到后 回复 确认帧
            d = ZDSBSJ()
            rst = d.unpack(data[1:])
        elif t == 1:
            #1: 中心下发停止充电指令 数据定义见附表 5.7.27
            d = ZXXFJS()
            rst = d.unpack(data[1:])
        elif t == 2:
            #2: 中心下发强制停止充电指令 数据定义见附表 5.7.28
            d = ZXQZJS()
            rst = d.unpack(data[1:])
        return rst

class P_AC_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #1:读取参数数据，下行
            pass
        elif t == 2:
            #2:读取参数返回数据，上行
            pass
        elif t == 3:
            #3:设置参数数据，下行
            pass
        elif t == 4:
            #4:设置参数返回数据
            pass
        return rst
        

class P_AB_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1>: = 预约下行数据
            d = CDYYXXSJ()
            rst = d.unpack(data[1:])
        elif t == 2:
            #<2>: = 预约上行数据
            d = CDYYSXSJ()
            rst = d.unpack(data[1:])
        elif t == 3:
            #<3>: = 取消下行数据
            d = QXYYXXSJ()
            rst = d.unpack(data[1:])
        elif t == 4:
            #<4>: = 取消上行数据
            d = QXYYSXSJ()
            rst = d.unpack(data[1:])
        elif t == 5:
            #<5>: = 查询下行数据
            d = YYCXXXSJ()
            rst = d.unpack(data[1:])
        elif t == 6:
            #<6>: = 查询上行数据
            d = YYCXSXSJ()
            rst = d.unpack(data[1:])
        return rst

class P_AF_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1>: = 蓝牙状态
            pass
        elif t == 2:
            #<2>: = 打开蓝牙
            pass
        elif t == 3:
            #<3>: = 关闭蓝牙
            pass
        elif t == 4:
            #<4>: = 其它数据
            pass
        return rst

class P_AD_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1>: = 蓝牙状态
            pass
        elif t == 2:
            #<2>: = 打开地锁
            pass
        elif t == 3:
            #<3>: = 关闭地锁
            pass
        elif t == 4:
            #<4>: = 其它数据
            pass
        return rst

class P_AE_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1> := 软件升级激活下行数据
            d = RJSJJHXXSJ()
            rst = d.unpack(data[1:])
        elif t == 2:
            #<2> := 软件升级激活确认上行数据
            d = RJSJJHSXSJ()
            rst = d.unpack(data[1:])
        elif t == 3:
            #<3> := 软件升级上行请求数据
            d = DZRJSJSXSJ()
            rst = d.unpack(data[1:])
        elif t == 4:
            #<4> := 软件升级下行应答数据
            d = RJSJXXYDSJ()
            rst = d.unpack(data[1:])
        return rst

class P_WS_NA_1(ASDU):
    def __init__(self):
        ASDU.__init__(self)

    def unpack(self, data):
        data = ASDU.unpack(self, data)
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            print("")

    def unpack_sq0(self, data):
        t = struct.unpack('B', data[0])[0]
        if t == 1:
            #<1>: = 工作模式切换下行数据
            d = GZMSQHXXSJ()
            rst = d.unpack(data[1:])
        elif t == 2:
            #<2>: = 工作模式切换上行数据
            d = GZMSQHSXSJ()
            rst = d.unpack(data[1:])
        elif t == 3:
            #<3>: = 工作模式查询下行数据
            d = GZMSCXXXSJ()
            rst = d.unpack(data[1:])
        elif t == 4:
            #<4>: = 工作模式查询上行数据
            d = GZMSCXSXSJ()
            rst = d.unpack(data[1:])
        return rst

class MsgDesc:
    def __init__(self, name, t, length, default_value):
        self.msg_name = name
        self.msg_type = t
        self.msg_len = length
        self.msg_default_value = default_value

class BaseMsg(BaseCMD):
    def __init__(self):
        BaseCMD.__init__(self)
        self.props = []
        self.values = {}

    def set_value(key, value):
        self.values[key] = value

    def get_value(key):
        if(self.values.has_key(key)):
            return self.values[key]
        for p in self.props:
            if(p.msg_name == key):
                return p.msg_default_value

    def unpack(self, data):
        offset  = 0
        for p in self.props:
            if p.msg_type == 'B':
                v = struct.unpack('B', data[offset])[0]
                self.values[p.msg_name] = v
                offset = offset + 1
                continue
            if p.msg_type == 'I':
                v = struct.unpack(BYTE_ORDER + 'I', data[offset:offset + 4])
                self.values[p.msg_name] = v
                offset = offset + 4
                continue
            if p.msg_type == 'BCD':
                v = self.decode_bcd(data[offset:offset + p.msg_len])
                self.values[p.msg_name] = v
                offset = offset + p.msg_len
                continue
            if p.msg_type == 'H':
                v = struct.unpack(BYTE_ORDER + 'H', data[offset:offset + 2])
                self.values[p.msg_name] = v
                offset = offset + 2
                continue
            if p.msg_type == 'STR':
                v = data[offset:offset + p.msg_len]
                self.values[p.msg_name] = v
                offset = offset + p.msg_len
                continue
            if p.msg_type == 'CP56Time':
                _a = CP56Time()
                _a.unpack(data[offset:offset + 7])
                self.values[p.msg_name] = _a
                offset = offset + 7
                continue
        return data[offset:]

    def pkg(self):
        d = ''
        for p in self.props:
            if p.msg_type == 'B':
                d = d + struct.pack('B', self.values[p.msg_name])
            if p.msg_type = 'I':
                d = d + struct.pack(BYTE_ORDER + 'I', self.values[p.msg_name])
            if p.msg_type == 'H':
                d = d + struct.pack(BYTE_ORDER + 'H', self.values[p.msg_name])
            if p.msg_type = 'BCD':
                d = d + self.encode_bcd(self.values[p.msg_name])
            if p.msg_type == 'STR':
                d = d + self.values[p.msg_name]
            if p.msg_type == 'CP56Time':
                self.values[p.msg_name].pkg()
                d = d + self.values[p.msg_name].data
        self.data = d

class CDSCSJ(BaseMsg):
    '''5.7.1充电过程实时监测数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('CDSCDY', 'H', 2, 0)) #充电输出电压 精确到小数点后一位
        self.props.append(MsgDesc('CDSCDL', 'H', 2, 0)) #充电输出电流 精确到小数点后二位
        self.props.append(MsgDesc('SCJDQZT', 'B', 1, 0)) #输出继电器状态 布尔型, 变化上传;0 关，1 开
        self.props.append(MsgDesc('LJQRKGZT', 'B', 1, 0)) #连接确认开关状态 布尔型, 变化上传;0 关，1 开
        self.props.append(MsgDesc('YGZDD', 'I', 4, 0)) #有功总电度 精确到小数点后两位
        self.props.append(MsgDesc('CDZBH', 'BCD', 8, '0123456701234567')) #充电桩编号 16 位设备编码
        self.props.append(MsgDesc('SFLJDC', 'B', 1, 0)) #是否连接电池 布尔型, 变化上传，0: 否，1:是
        self.props.append(MsgDesc('GZZT', 'BCD', 2, '0000')) #工作状态 0 离 线 ，1 故 障 ，2 待 机 3 工作 4预约 5 等待
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 充电枪编号
        self.props.append(MsgDesc('CDQLX', 'B', 1, 0)) #充电类型 0 交流 1 直流
        self.props.append(MsgDesc('GZYYDM', 'B', 1, 0)) #故障原因代码 故障代码见 5.4.4.5，如 13 代表充电中强行拔 枪,无故障填 0

class JQSJ(BaseMsg):
    '''5.7.2鉴权数据包'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '0123456701234567')) #终端机器编码 充电桩资产编号，系统参 数的编号
        self.props.append(MsgDesc('LJKH', 'BCD', 8, '0123456701234567')) #物理卡号 16 位编码
        self.props.append(MsgDesc('KMM', 'STR', 16, '0123456701234567')) #卡密码 16 位字符串，同输入密 码相同
        self.props.append(MsgDesc('SRMM', 'STR', 16, '0123456701234567')) #卡密码 16 位字符串
        self.props.append(MsgDesc('KYE', 'I', 4, 0)) #卡余额 精确到小数点后两位，不 需要填写
        self.props.append(MsgDesc('KZT', 'H', 2, 0)) #卡状态 0001-正常 0002-挂失 0003-欠费 0004-锁定 0005-注销，不需要填写
        self.props.append(MsgDesc('DDQCWYBS', 'STR', 32, '')) #电动汽车唯一标识 32 位编码 前五位是组织机构编码，不需要填写
        self.props.append(MsgDesc('JFMXBM', 'BCD', 8, '0123456701234567')) #计费模型编码 8 位编码，不需要填写
        self.props.append(MsgDesc('DDCCPHM', 'STR', 18, '')) #电动车车牌号码 18 位字符串,GBK 编码 没有值时用’\0’填充
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 整型，0-255，0 表示单 枪或任意枪
        self.props.append(MsgDesc('SJJYY', 'STR', 16, '')) #数据校验域 见 6.3 安全校验域的计 算方法

class TZCDSJ(BaseMsg):
    '''5.7.3在线情况下停止充电时上传记录数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('JYLSH', 'BCD', 16, '')) #交易流水号 32 位交易代码
        self.props.append(MsgDesc('YWLX', 'BCD', 2, '')) #业务类型 0001-交流充电 0002-换电 0003 直流充电
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 充电桩资产编号，系统参数 的编号
        self.props.append(MsgDesc('YHBH', 'BCD', 8, '')) #用户编号 16 位设备编码,不需要填写
        self.props.append(MsgDesc('LJKH', 'BCD', 8, '')) #物理卡号 16 位编码
        self.props.append(MsgDesc('KSSJ', 'CP56Time', 7, CP56Time())) #开始时间 CP56Time2a 格式
        self.props.append(MsgDesc('JSSJ', 'CP56Time', 7, CP56Time())) #结束时间 CP56Time2a 格式
        self.props.append(MsgDesc('JQSZ', 'I', 4, 0)) #尖起示值 精确到小数点后二位
        self.props.append(MsgDesc('JZSZ', 'I', 4, 0)) #尖止示值 精确到小数点后二位
        self.props.append(MsgDesc('FQSZ', 'I', 4, 0)) #峰起示值 精确到小数点后二位
        self.props.append(MsgDesc('FZSZ', 'I', 4, 0)) #峰止示值 精确到小数点后二位
        self.props.append(MsgDesc('PQSZ', 'I', 4, 0)) #平起示值 精确到小数点后二位
        self.props.append(MsgDesc('PZSZ', 'I', 4, 0)) #平止示值 精确到小数点后二位
        self.props.append(MsgDesc('GQSZ', 'I', 4, 0)) #谷起示值 精确到小数点后二位
        self.props.append(MsgDesc('GZSZ', 'I', 4, 0)) #谷止示值 精确到小数点后二位
        self.props.append(MsgDesc('JDL', 'I', 4, 0)) #尖电量 精确到小数点后二位
        self.props.append(MsgDesc('FDL', 'I', 4, 0)) #峰电量 精确到小数点后二位
        self.props.append(MsgDesc('PDL', 'I', 4, 0)) #平电量 精确到小数点后二位
        self.props.append(MsgDesc('GDL', 'I', 4, 0)) #谷电量 精确到小数点后二位
        self.props.append(MsgDesc('ZDL', 'I', 4, 0)) #总电量 精确到小数点后二位
        self.props.append(MsgDesc('JLSSLX', 'BCD', 2, 0)) #计量示数类型 0001-里程 0002-充电量 0003-放电量
        self.props.append(MsgDesc('BCJLSS', 'I', 4, 0)) #本次计量示数 精确到小数点后二位，不需 要填写
        self.props.append(MsgDesc('SCJLSS', 'I', 4, 0)) #上次计量示数 精确到小数点后二位，不需 要填写
        self.props.append(MsgDesc('SCCHDZBH', 'BCD', 5, 0)) #上次充换电站 编号 9位部门编码 离散充电桩 附加集中器模式上传桩编 号前 5 位，不需要填写
        self.props.append(MsgDesc('SCYWLX', 'BCD', 2, 0)) #上次业务类型 0001-充电 0002-换电，不 需要填写
        self.props.append(MsgDesc('DDQCWYBS', 'STR', 32, 0)) #电动汽车唯一 标识 32 位编码 前五位是组织机构编码，不 需要填写
        self.props.append(MsgDesc('JGE', 'I', 4, 0)) #尖金额 精确到小数点后两位
        self.props.append(MsgDesc('FJE', 'I', 4, 0)) #峰金额 精确到小数点后两位
        self.props.append(MsgDesc('PJE', 'I', 4, 0)) #平金额 精确到小数点后两位
        self.props.append(MsgDesc('GJE', 'I', 4, 0)) #谷金额 精确到小数点后两位
        self.props.append(MsgDesc('ZJE', 'I', 4, 0)) #总金额 精确到小数点后二位
        self.props.append(MsgDesc('DDCCPHM', 'STR', 18, 0)) #电动车车牌号 码 18 位字符串，GBK 编码
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 充电枪编号
        self.props.append(MsgDesc('YYLSH', 'STR', 20, '')) #预约流水号 预约流水号
        self.props.append(MsgDesc('SJJYY', 'STR', 16, '')) #数据校验域 见 6.3 安全校验域的计算 方法

class SCJYSJ(BaseMsg):
    '''5.7.4离线交易上线后上传交易记录数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '0123456701234567')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('JYLSH', 'BCD', 16, '')) #交易流水号 32 位交易代码
        self.props.append(MsgDesc('YHBH', 'BCD', 8, '')) #用户编号 16 位设备编码,不需要填写
        self.props.append(MsgDesc('LJKH', 'BCD', 8, '')) #逻辑卡号 16 位编码
        self.props.append(MsgDesc('LXJYLX', 'BCD', 1, '')) #离线交易类型 1:交流充电 2:换电 3: 直流充电
        self.props.append(MsgDesc('KSSJ', 'CP56Time', 7, CP56Time())) #开始时间 CP56Time2a 格式
        self.props.append(MsgDesc('JSSJ', 'CP56Time', 7, CP56Time())) #结束时间 CP56Time2a 格式
        self.props.append(MsgDesc('JQSZ', 'I', 4, 0)) #尖起示值 精确到小数点后二位
        self.props.append(MsgDesc('JZSZ', 'I', 4, 0)) #尖止示值 精确到小数点后二位
        self.props.append(MsgDesc('FQSZ', 'I', 4, 0)) #峰起示值 精确到小数点后二位
        self.props.append(MsgDesc('FZSZ', 'I', 4, 0)) #峰止示值 精确到小数点后二位
        self.props.append(MsgDesc('PQSZ', 'I', 4, 0)) #平起示值 精确到小数点后二位
        self.props.append(MsgDesc('PZSZ', 'I', 4, 0)) #平止示值 精确到小数点后二位
        self.props.append(MsgDesc('GQSZ', 'I', 4, 0)) #谷起示值 精确到小数点后二位
        self.props.append(MsgDesc('GZSZ', 'I', 4, 0)) #谷止示值 精确到小数点后二位
        self.props.append(MsgDesc('JLLX', 'BCD', 2, 0)) #计量类型 0001-里程 0002-充 电量 0003-放电量
        self.props.append(MsgDesc('BCJLSS', 'I', 4, 0)) #本次计量示数 精确到小数点后二位
        self.props.append(MsgDesc('SCJLSS', 'I', 4, 0)) #上次计量示数 精确到小数点后二位
        self.props.append(MsgDesc('GDL', 'I', 4, 0)) #尖电量 精确到小数点后二位
        self.props.append(MsgDesc('GGE', 'I', 4, 0)) #尖金额 精确到小数点后两位
        self.props.append(MsgDesc('FDL', 'I', 4, 0)) #峰电量 精确到小数点后二位
        self.props.append(MsgDesc('FJE', 'I', 4, 0)) #峰金额 精确到小数点后两位
        self.props.append(MsgDesc('PDL', 'I', 4, 0)) #平电量 精确到小数点后二位
        self.props.append(MsgDesc('PJE', 'I', 4, 0)) #平金额 精确到小数点后两位
        self.props.append(MsgDesc('GDL', 'I', 4, 0)) #谷电量 精确到小数点后二位
        self.props.append(MsgDesc('GJE', 'I', 4, 0)) #谷金额 精确到小数点后两位
        self.props.append(MsgDesc('ZDL', 'I', 4, 0)) #总电量 精确到小数点后二位
        self.props.append(MsgDesc('YWLX', 'BCD', 2, 0)) #业务类型 0001-交流充电 0002-换电 0003 直 流充电
        self.props.append(MsgDesc('XFSZ', 'I', 4, 0)) #消费数值 精确到小数点后二位
        self.props.append(MsgDesc('XFDJ', 'I', 4, 0)) #消费单价 精确到小数点后二位
        self.props.append(MsgDesc('XFJE', 'I', 4, 0)) #消费金额 精确到小数点后两位
        self.props.append(MsgDesc('DDQCWYBS', 'STR', 32, 0)) #电动汽车唯一 标识 32 位编码 前五位是组织机构编码
        self.props.append(MsgDesc('DDCCPHM', 'STR', 18, 0)) #电动车车牌号 码 18 位字符串，GBK 编码
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 充电枪编号
        self.props.append(MsgDesc('SJJYY', 'STR', 16, '')) #数据校验域 见 6.3 安全校验域的计算 方法

class HMDXFSJ(BaseMsg):
    '''5.7.5黑名单下发时下行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('LJKH', 'BCD', 8, '')) #逻辑卡号 16 位编码
        self.props.append(MsgDesc('ZT', 'BCD', 2, '0123')) #状态 0001-挂失 0002-解挂
        self.props.append(MsgDesc('ZHGXSJ', 'CP56Time', 7, CP56Time())) #最后更新时间 CP56Time2a 格式
        self.props.append(MsgDesc('DDCCPHM', 'STR', 18, 0)) #电动车车牌号 码 18 位字符串，GBK 编码

class XFBZFLSJ(BaseMsg):
    '''5.7.6下发标准费率'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('SXSJ', 'CP56Time', 7, CP56Time())) #生效时间 CP56Time2a 格式
        self.props.append(MsgDesc('SXSJ', 'CP56Time', 7, CP56Time())) #失效时间 CP56Time2a 格式
        self.props.append(MsgDesc('ZXZT', 'BCD', 2, '0123')) #执行状态 0001-有效 0002-无效
        self.props.append(MsgDesc('JLLX', 'BCD', 2, '0123')) #计量类型 0001-里程 0002-充电 量 0003-放电量
        self.props.append(MsgDesc('JDJ', 'I', 4, 0)) #尖电价 精确到小数点后五位
        self.props.append(MsgDesc('FDJ', 'I', 4, 0)) #峰电价 精确到小数点后五位
        self.props.append(MsgDesc('PDJ', 'I', 4, 0)) #平电价 精确到小数点后五位
        self.props.append(MsgDesc('GDJ', 'I', 4, 0)) #谷电价 精确到小数点后五位

class JQXXSJ(BaseMsg):
    '''5.7.7鉴权下行/APP 充电激活数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '0123456701234567')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('LJKH', 'BCD', 8, '')) #逻辑卡号 16 位编码
        self.props.append(MsgDesc('DDQCWYBS', 'STR', 32, 0)) #电动汽车唯一 标识 32 位编码 前五位是组织机构编码
        self.props.append(MsgDesc('JFMXBM', 'BCD', 8, '')) #计费模型编码 8 位编码
        self.props.append(MsgDesc('KKHKYE', 'I', 4, 0)) #扣款后卡余额 精确到小数点后两位
        self.props.append(MsgDesc('JQCGBZ', 'B', 1, 0)) #鉴权成功标志 布尔型(1，鉴权成功; 0，鉴权失败)
        self.props.append(MsgDesc('JQSBYY', 'BCD', 2, '')) #鉴权失败原因 0000-成功 0001-账户余额不足 0002-套餐余额不足 0003-非法用户 0004- 挂失卡 0005-车卡不 匹配
        self.props.append(MsgDesc('SYLC', 'I', 4, 0)) #剩余里程 精确到小数点后两位
        self.props.append(MsgDesc('SYDL', 'I', 4, 0)) #剩余电量 精确到小数点后两位
        self.props.append(MsgDesc('SYCS', 'I', 4, 0)) #剩余次数 精确到小数点后两位
        self.props.append(MsgDesc('DDCCPHM', 'STR', 18, '')) #电动车车牌号码 18 位字符串
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0-255，0 表示单枪， 多枪时从 1 开始编号
        self.props.append(MsgDesc('YYBH', 'BCD', 10, '')) #预约编号 20 位预约编号
        self.props.append(MsgDesc('SJJYY', 'STR', 16, '')) #数据校验域 见 6.3 安全校验域的 计算方法

class KKHXXSJ(BaseMsg):
    '''5.7.8扣款后下行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '0123456701234567')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('LJKH', 'BCD', 8, '')) #逻辑卡号 16 位编码
        self.props.append(MsgDesc('KKJE', 'I', 4, 0)) #扣款金额 精确到小数点后两位
        self.props.append(MsgDesc('ZHYE', 'I', 4, 0)) #帐户余额 精确到小数点后两位
        self.props.append(MsgDesc('KKCGBZ', 'B', 1, 0)) #扣款成功标志 布尔型,(1，扣款成功， 0 扣款失败)
        self.props.append(MsgDesc('KKSBYY', 'BCD', 2, '')) #扣款失败原因 0000-成功 0001-账户余额不足 0002-套餐余额不足 0003-交易相同 0004- 挂失卡 0005-车卡不 匹配
        self.props.append(MsgDesc('KCLC', 'I', 4, 0)) #扣除里程 精确到小数点后两位
        self.props.append(MsgDesc('SYLC', 'I', 4, 0)) #剩余里程 精确到小数点后两位
        self.props.append(MsgDesc('KCDL', 'I', 4, 0)) #扣除电量 精确到小数点后两位
        self.props.append(MsgDesc('SYDL', 'I', 4, 0)) #剩余电量 精确到小数点后两位
        self.props.append(MsgDesc('KCCS', 'I', 4, 0)) #扣除次数 精确到小数点后两位
        self.props.append(MsgDesc('SYCS', 'I', 4, 0)) #剩余次数 精确到小数点后两位
        self.props.append(MsgDesc('DDCCPHM', 'STR', 18, '')) #电动车车牌号码 18 位字符串
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0-255，0 表示单枪， 多枪时从 1 开始编号
        self.props.append(MsgDesc('SJJYY', 'STR', 16, '')) #数据校验域 见 6.3 安全校验域的 计算方法

class CSSJ(BaseMsg):
    '''5.7.9参数数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('CSDM', 'BCD', 2, '')) #参数代码 见表 5-35 中代码
        self.props.append(MsgDesc('CSZCD', 'B', 1, 0)) #参数值长度 参数实际长度
        self.props.append(MsgDesc('CSZ', 'STR', 64, '')) #参数值 实际长度见表 5-35，不 够 64bytes 在后面补零

class FDDLSDSZ(BaseMsg):
    '''5.7.10分段电量时段设置'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('JDLKSSJ1', 'BCD', 2, '')) #尖电量时段开始时间 1
        self.props.append(MsgDesc('JDLJSSJ1', 'BCD', 2, '')) #尖电量时段结束时间 1
        self.props.append(MsgDesc('JDLKSSJ2', 'BCD', 2, '')) #尖电量时段开始时间 2
        self.props.append(MsgDesc('JDLJSSJ2', 'BCD', 2, '')) #尖电量时段结束时间 2
        self.props.append(MsgDesc('FDLKSSJ1', 'BCD', 2, '')) #峰电量时段开始时间 1
        self.props.append(MsgDesc('FDLJSSJ1', 'BCD', 2, '')) #峰电量时段结束时间 1
        self.props.append(MsgDesc('FDLKSSJ2', 'BCD', 2, '')) #峰电量时段开始时间 2
        self.props.append(MsgDesc('FDLJSSJ2', 'BCD', 2, '')) #峰电量时段结束时间 2
        self.props.append(MsgDesc('PDLKSSJ1', 'BCD', 2, '')) #平电量时段开始时间 1
        self.props.append(MsgDesc('PDLJSSJ1', 'BCD', 2, '')) #平电量时段结束时间 1
        self.props.append(MsgDesc('PDLKSSJ2', 'BCD', 2, '')) #平电量时段开始时间 2
        self.props.append(MsgDesc('PDLJSSJ2', 'BCD', 2, '')) #平电量时段结束时间 2
        self.props.append(MsgDesc('GDLKSSJ1', 'BCD', 2, '')) #谷电量时段开始时间 1
        self.props.append(MsgDesc('GDLJSSJ1', 'BCD', 2, '')) #谷电量时段结束时间 1
        self.props.append(MsgDesc('GDLKSSJ2', 'BCD', 2, '')) #谷电量时段开始时间 2
        self.props.append(MsgDesc('GDLJSSJ2', 'BCD', 2, '')) #谷电量时段结束时间 2

class CDYYXXSJ(BaseMsg):
    '''5.7.11充电预约下行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('JYLSH', 'BCD', 10, '')) #交易流水号 20 位交易代码，预约号
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('YHKH', 'BCD', 8, '')) #用户卡号 16 位卡号或账户
        self.props.append(MsgDesc('CPHM', 'STR', 18, '')) #车牌号码 车牌号码 GBK 编码
        self.props.append(MsgDesc('CDLX', 'B', 1, 0)) #充电类型 0 交流充电 1 直流充电 2 不限类型
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0 不限或者单枪 其它表示具体的枪编号
        self.props.append(MsgDesc('YYKSSJ', 'CP56Time', 7, CP56Time())) #预约开始时间 cp56time2a 各式
        self.props.append(MsgDesc('YYCDCL', 'BCD', 2, '')) #预约充电策略 0 充满为止 1 预约电度 2 预约时间 3 预约充电电量
        self.props.append(MsgDesc('YYCDCS', 'H', 2, 0)) #预约策略参数 策略 1 时表示电度，单位 kwh，2 时间，单位分钟， 3 充电电量，单位 ah(安时)

class CDYYSXSJ(BaseMsg):
    '''5.7.12充电预约上行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('JYLSH', 'BCD', 10, '')) #交易流水号 20 位交易代码，预约号
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('YHKH', 'BCD', 8, '')) #用户卡号 16 位卡号或账户
        self.props.append(MsgDesc('CPHM', 'STR', 18, '')) #车牌号码 车牌号码 GBK 编码
        self.props.append(MsgDesc('CDLX', 'B', 1, 0)) #充电类型 0 交流充电 1 直流充电 2 不限类型
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0 不限或者单枪 其它表示具体的枪编号
        self.props.append(MsgDesc('YYKSSJ', 'CP56Time', 7, CP56Time())) #预约开始时间 cp56time2a 各式
        self.props.append(MsgDesc('YYCDCL', 'BCD', 2, '')) #预约充电策略 0 充满为止 1 预约电度 2 预约时间 3 预约充电电量
        self.props.append(MsgDesc('YYCDCS', 'H', 2, 0)) #预约策略参数 策略 1 时表示电度，单位 kwh，2 时间，单位分钟， 3 充电电量，单位 ah(安时)
        self.props.append(MsgDesc('YYJG', 'BCD', 2, '')) #预约结果 0000 预约成功 0003 已经被预约或预约 时间冲突 其它错误码见 5.4.4.7

class QXYYXXSJ(BaseMsg):
    '''5.7.13取消预约下行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('JYLSH', 'BCD', 10, '')) #交易流水号 20 位交易代码，预约号
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('YHKH', 'BCD', 8, '')) #用户卡号 16 位卡号或账户
        self.props.append(MsgDesc('CPHM', 'STR', 18, '')) #车牌号码 车牌号码 GBK 编码
        self.props.append(MsgDesc('CDLX', 'B', 1, 0)) #充电类型 0 交流充电 1 直流充电 2 不限类型
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0 不限或者单枪 其它表示具体的枪编号
        self.props.append(MsgDesc('YYKSSJ', 'CP56Time', 7, CP56Time())) #预约开始时间 cp56time2a 各式
        self.props.append(MsgDesc('YYCDCL', 'BCD', 2, '')) #预约充电策略 0 充满为止 1 预约电度 2 预约时间 3 预约充电电量
        self.props.append(MsgDesc('YYCDCS', 'H', 2, 0)) #预约策略参数 策略 1 时表示电度，单位 kwh，2 时间，单位分钟， 3 充电电量，单位 ah(安时)

class QXYYSXSJ(BaseMsg):
    '''5.7.14取消预约上行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('JYLSH', 'BCD', 10, '')) #交易流水号 20 位交易代码，预约号
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('YHKH', 'BCD', 8, '')) #用户卡号 16 位卡号或账户
        self.props.append(MsgDesc('CPHM', 'STR', 18, '')) #车牌号码 车牌号码 GBK 编码
        self.props.append(MsgDesc('CDLX', 'B', 1, 0)) #充电类型 0 交流充电 1 直流充电 2 不限类型
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0 不限或者单枪 其它表示具体的枪编号
        self.props.append(MsgDesc('YYKSSJ', 'CP56Time', 7, CP56Time())) #预约开始时间 cp56time2a 各式
        self.props.append(MsgDesc('YYCDCL', 'BCD', 2, '')) #预约充电策略 0 充满为止 1 预约电度 2 预约时间 3 预约充电电量
        self.props.append(MsgDesc('YYCDCS', 'H', 2, 0)) #预约策略参数 策略 1 时表示电度，单位 kwh，2 时间，单位分钟， 3 充电电量，单位 ah(安时)
        self.props.append(MsgDesc('QXJG', 'BCD', 2, '')) #取消结果代码 0000 取消成功 0001 预约已经失效 0002 预约号错误，取消 失败

class YYCXXXSJ(BaseMsg):
    '''5.7.15预约查询下行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('JYLSH', 'BCD', 10, '')) #交易流水号 20 位交易代码，预约号
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('YHKH', 'BCD', 8, '')) #用户卡号 16 位卡号或账户
        self.props.append(MsgDesc('CPHM', 'STR', 18, '')) #车牌号码 车牌号码 GBK 编码
        self.props.append(MsgDesc('YYKSSJ', 'CP56Time', 7, CP56Time())) #预约开始时间 cp56time2a 各式

class YYCXSXSJ(BaseMsg):
    '''5.7.16预约查询上行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('JYLSH', 'BCD', 10, '')) #交易流水号 20 位交易代码，预约号
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('YHKH', 'BCD', 8, '')) #用户卡号 16 位卡号或账户
        self.props.append(MsgDesc('CPHM', 'STR', 18, '')) #车牌号码 车牌号码 GBK 编码
        self.props.append(MsgDesc('CDLX', 'B', 1, 0)) #充电类型 0 交流充电 1 直流充电 2 不限类型
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0 不限或者单枪 其它表示具体的枪编号
        self.props.append(MsgDesc('YYKSSJ', 'CP56Time', 7, CP56Time())) #预约开始时间 cp56time2a 各式
        self.props.append(MsgDesc('YYCDCL', 'BCD', 2, '')) #预约充电策略 0 充满为止 1 预约电度 2 预约时间 3 预约充电 电量
        self.props.append(MsgDesc('YYCDCS', 'BCD', 2, '')) #预约充电策略参数 策略 1 时表示电度，单位 kwh，2 时间，单位分钟， 3 充电电量，单位 ah(安时)
        self.props.append(MsgDesc('CXJG', 'BCD', 2, '')) #查询结果 0000 预约查询成功 0001 预约不存在 其它错误码见 5.4.4.7


class JHCDSXSJ(BaseMsg):
    '''5.7.17 APP 激活充电上行数据(APP 专用)(133 指令)'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('LJKH', 'BCD', 8, '')) #用户卡号 16 位编码
        self.props.append(MsgDesc('DDCCPHM', 'STR', 18, '')) #电动车车牌号码 18 位字符串
        self.props.append(MsgDesc('CDLX', 'B', 1, 0)) #充电类型 0 交流充电 1 直流充 电
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 充电枪编号，0 单枪， 其它表示具体编号
        self.props.append(MsgDesc('JRCDZTCGBZ', 'B', 1, 0)) #进入充电状态成功标 志 布尔型,(1 成功，0 失 败)
        self.props.append(MsgDesc('JRCDZTCGBZSBYY', 'BCD', 2, '')) #进入充电状态失败原因代码 0000-成功 0001-正在充电 0002-设备故障

class RJSJJHXXSJ(BaseMsg):
    '''5.7.18软件升级激活下行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('RJBB', 'BCD', 2, '')) #软件版本 4 位编码
        self.props.append(MsgDesc('DWJDX', 'I', 4, 0)) #低位文件大小 整数，文件大小，单位: Byte
        self.props.append(MsgDesc('GWJDX', 'I', 4, 0)) #高位文件大小 整数，文件大小，单位: Byte
        self.props.append(MsgDesc('DWJJYM', 'STR', 32, '')) #低位文件校验码 文件内容做 MD5 HASH
        self.props.append(MsgDesc('GWJJYM', 'STR', 32, '')) #高位文件校验码 文件内容做 MD5 HASH
        self.props.append(MsgDesc('WJDM', 'STR', 32, '')) #文件代码 文件代码
        self.props.append(MsgDesc('WJMC', 'STR', 64, '')) #文件名称 文件名称

class RJSJJHSXSJ(BaseMsg):
    '''5.7.19软件升级激活确认上行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('RJBB', 'BCD', 2, '')) #软件版本 4 位编码
        self.props.append(MsgDesc('WJDM', 'STR', 32, '')) #文件代码 文件代码

class DZRJSJSXSJ(BaseMsg):
    '''5.7.20电桩软件升级上行请求数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('RJBB', 'BCD', 2, '')) #软件版本 4 位编码
        self.props.append(MsgDesc('WJDM', 'STR', 32, '')) #文件代码 文件代码
        self.props.append(MsgDesc('GDWBJ', 'B', 1, 0)) #高低位文件标志 0 低位，1 高位
        self.props.append(MsgDesc('PYL', 'I', 4, 0)) #偏移量 从文件起始的为止的 偏移量,第一帧数据为 0
        self.props.append(MsgDesc('length', 'I', 4, 0)) #长度 本次请求数据长度,保 证应答帧的总长度不 超过 255Bytes

class RJSJXXYDSJ(BaseMsg):
    '''5.7.21软件升级下行应答数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('PYL', 'I', 4, 0)) #偏移量 从文件起始的为止的 偏移量,第一帧数据为 0
        self.props.append(MsgDesc('WJNRCD', 'I', 4, 0)) #文件内容长度 本次应答数据长度
        self.props.append(MsgDesc('DATA', 'STR', 0, '')) #数据内容 按照 WJNRCD 应答，文 件不存在或者其它错 误以及到达文件末尾 原因时，文件内容长度 为0
        self.props.append(MsgDesc('CRC', 'H', 2, 0)) #数据 CRC 校验 应答数据的 CRC16 校验 值

        #self.DATA = data[16:16 + self.WJNRCD]
        #self.CRC = data[16 + self.WJNRCD:16 + self.WJNRCD + 2]
        #return data[16 + self.WJNRCD + 2:]

class GZMSQHXXSJ(BaseMsg):
    '''5.7.22工作模式切换下行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('GZMS', 'BCD', 2, '')) #工作模式 4 位编码 0001 工作模式 0002 管理模式

class GZMSQHSXSJ(BaseMsg):
    '''5.7.23工作模式切换上行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('GZMS', 'BCD', 2, '')) #工作模式 4 位编码 0001 工作模式 0002 管理模式
        self.props.append(MsgDesc('MSQHJG', 'BCD', 2, '')) #模式切换结果 模式切换结果 0000 成功 0001 升级过程中不能切换 0002 充电过程中不允许切换 0003 预约中不能切换为管理模式 0099 其它错误

class GZMSCXXXSJ(BaseMsg):
    '''5.7.24工作模式查询下行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码

class GZMSCXSXSJ(BaseMsg):
    '''5.7.25工作模式查询上行数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('GZMS', 'BCD', 2, '')) #工作模式 4 位编码 0001 工作模式 0002 管理模式

class ZDSBSJ(BaseMsg):
    '''5.7.26主动上报数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('XXDM', 'B', 1, 0)) #消息代码
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0 表示单枪或者不需要

class ZXXFJS(BaseMsg):
    '''5.7.27中心下发结束充电/开锁数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('YHKH', 'BCD', 8, '')) #用户卡号 16 用户卡号/账号
        self.props.append(MsgDesc('XXDM', 'B', 1, 0)) #消息代码 定义见 5.4.5
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0 表示单枪或者不需要

class ZXQZJS(BaseMsg):
    '''5.7.28中心强制结束充电数据'''
    def __init__(self):
        BaseMsg.__init__(self)
        self.props.append(MsgDesc('ZDJQBM', 'BCD', 8, '')) #终端机器编码 16 位设备编码
        self.props.append(MsgDesc('YHKH', 'BCD', 8, '')) #用户卡号 16 用户卡号/账号
        self.props.append(MsgDesc('XXDM', 'B', 1, 0)) #消息代码 0xFF
        self.props.append(MsgDesc('CDQBH', 'B', 1, 0)) #充电枪编号 0 表示单枪或者不需要

class BaseProtocol:

    def decode(self, stream):
        if len(stream) < 6:
            return
        rst = self.do_decode(stream)
        return rst

    def do_decode(self, stream):
        print 'stream len', len(stream)
        if stream[0] != '\x68':
            return
        _len = struct.unpack('B', stream[1])[0]
        _rlen = _len - 2 #去除0x68头和长度所占位置
        pkg = stream[0:_len]
        apdu = APDU() 
        data = apdu.unpack(pkg)
        return True, apdu, stream[_len:]

    def encode(self, cmd_data):
        pkg = ''
        pkg = cmd_data.data
        return pkg

