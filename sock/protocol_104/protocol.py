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
    def unpack(self, data):
        self.ms = data[0:2]
        self.minute = data[2:3]
        self.clock = data[3:4]
        self.day = data[4:5]
        self.month = data[5:6]
        self.year = data[6:7]
        return data[7:]

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
    self.SPI = 0
    self.RES = 0
    self.BL = 0
    self.SB = 0
    self.NT = 0
    self.IV = 0

    def unpack(self, data):
        v = struct.unpack('B', data[0])
        return data[1:]


class SVA(BaseCMD):
    '''
    5.4.2.9 标度化值(SVA)

    SVA:=F16[1..16]<-215..+215-1>
    没有定义测量值的分辩率，如果测量值的分辩率比 LSB 的最小单位粗，则这些 LSB 位设置为零。
    '''
    self.SVA = 0

    def unpack(self, data):
        lsb = data[0]
        hsb = data[1]
        return data[2:]

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
    self.OV = 0
    self.RES = 0
    self.BL = 0
    self.SB = 0
    self.NT = 0
    self.IV = 0

    def unpack(self, data):
        v = struct.unpack('B', data[0])
        return data[1:]

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
    self.COUNTER = 0
    self.SEQ = []

    def unpack(self, data):
        counter = struct.unpack(BYTE_ORDER + 'I', data[0:4])
        SQ_CY_CA_IV= struct.unpack('B', data[4])
        return data[5:]


class QOI(BaseCMD):
    '''
    5.4.2.12召唤限定词

    改变当地参数后的初始化(QOI) (TYPE 1.1) 
    QOI:=UI[1..8\<0..255>
    <0>:=未用 
    <1..19>:=为本配套标准的标准定义保留(兼容范围) 
    <20>:=响应站召唤
    '''
    self.QOI = 0

    def unpack(self, data):
        v = data[0]
        return data[1:]

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
    self.RQT = 0
    self.FRZ = 0

    def unpack(self, data):
        qcc = struct.unpack('B', data[0])
        return data[1:]
    
class APDU(BaseCMD):
    self.start_flag = 0
    self.apdu_len = 0 #max length 253
    self.apci = None
    self.asdu = None

    def unpack(self, data):
        self.start_flag = struct.unpack('B', data[0:1])
        self.apdu_len = struct.unpack('B', data[1:2])
        self.apci = APCI()
        data = self.apci.unpack(data[2:])
        self.asdu = ASDU()
        self.asdu.unpack(data)

    def pkg(self):
        pkg = ''
        pkg = pkg + struct.pack('B', self.start_flag)
        d = ''
        if self.apci is not None:
            self.apci.pkg()
            d = d + self.apci.data
        if self.asdu is not None:
            self.asdu.pkg()
            d = d + self.asdu.data
        _l = len(d)
        _l = _l + 2
        self.apdu_len = _l
        pkg = pkg + struct.pack('B', self.apdu_len)
        pkg = pkg + d
        self.data = pkg
    
class APCI(BaseCMD):
    self.i = None
    self.u = None
    self.s = None

    def unpack(self, data):
        one = struct.unpack('B', data[0])
        two = struct.unpack('B', data[1])
        three = struct.unpack('B', data[2])
        four = struct.unpack('B', data[3])
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
    self.send_sn = 0 #little-endian len 2 byte
    self.recv_sn = 0 #little-endian len 2 byte

    def pkg(self):
        self.data = struct.pack(BYTE_ORDER + 'H', self.send_sn)
        self.data = self.data + struct.pack(BYTE_ORDER + 'H', self.recv_sn)
    
class S(BaseCMD):#for watch info
    self.one = 1
    self.two = 0
    self.recv_sn = 0 #little-endian len 2 byte

    def pkg(self):
        self.data = struct.pack('B', self.one)
        self.data = self.data + struct.pack('B', self.two)
        self.data = self.data + struct.pack(BYTE_ORDER + 'H', self.recv_sn)
    
class U(BaseCMD):#for other control info no sid
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
    self.asdu_type = 0 #len 1 byte
    self.var_struct = 0 #len 1 byte for meta info count range 0-127 [1..7]  [8] is SQ
    self.cause = 0  #len 2 byte [1..8]
    self.common_addr = 0 #len 2 byte  0:not use  65535:global_addr  1-65534:stage_addr
    self.SQ = 0
    self.info_num = 0
    self.sub_asdu = None

    def get_info_addr(self, data):
        ia0 = struct.unpack(BYTE_ORDER + 'B', data[0])
        ia1 = struct.unpack(BYTE_ORDER + 'B', data[1])
        ia2 = struct.unpack(BYTE_ORDER + 'B', data[2])
        ia = ia0 << 16 + ia1 << 8 + ia2
        return ia

    def do(self):
        if self.sub_asdu is not None:
            self.sub_asdu.do()
    
    def pkg(self):
        if self.sub_asdu is not None:
            self.sub_asdu.pkg()
            self.data = self.sub_asdu.data
        else:
            self.data = ''

    def unpack(self, data):
        self.asdu_type = struct.unpack('B', data[0])
        self.var_struct = struct.unpack('B', data[1])
        self.cause = struct.unpack(BYTE_ORDER + 'H', data[2:4])
        self.common_addr = struct.unpack(BYTE_ORDER + 'H', data[4:6])
        self.SQ = self.var_struct & (1 << 7)
        self.info_num = self.var_struct >> 1
        self.cause = self.cause >> 8
        return data[6:]

    def unpack_subtype(self, data):
        self.sub_asdu = M_SP_NA_1()
        self.sub_asdu.asdu_type = self.asdu_type
        self.sub_asdu.var_struct = self.var_struct
        self.sub_asdu.cause = self.cause
        self.sub_asdu.common_addr = self.common_addr
        self.sub_asdu.SQ = self.SQ
        self.sub_asdu.info_num = self.info_num
        return self.sub_asdu.unpack(data)

class M_SP_NA_1(ASDU):
    self.info_addrs = []
    self.infos = []

    def pkg(self):
        pass

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)   
        pass

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 1
        end = 3
        while i <= self.info_num:
            info = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 4 + i * step])
            self.infos.append(info)
            end = 4 + i * step
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 4
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            info = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 4 + i * step])
            end = 4 + i * step
            self.info.append(info)
            i = i + 1
        return data[end:]

class M_ME_NA_1(ASDU):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 3
        end = 3
        while i <= self.info_num:
            value = struct.unpack(BYTE_ORDER + 'H', data[3 + i * step : 5 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[5 + i * step : 6 + i * step])
            end = 6 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 6
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = struct.unpack(BYTE_ORDER + 'H', data[3 + i * step : 5 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[5 + i * step : 6 + i * step])
            end = 6 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class M_IT_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class M_RE_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos =  []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class M_CM_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class M_MD_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class M_SD_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class M_JC_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class C_IC_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class C_CI_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class C_CS_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class C_RP_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class C_CD_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class P_AC_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class P_AB_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class P_AF_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class P_AD_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class P_AE_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1 
        return data[end:]

class P_WS_NA_1(BaseCMD):
    self.info_addrs = []
    self.infos = []

    def unpack(self, data):
        if self.SQ == 0:
            return self.unpack_sq0(data)
        else:
            return self.unpack_sq1(data)

    def unpack_sq0(self, data):
        ia = self.get_info_addr(data[0:3])
        self.info_addrs.append(ia)
        i = 0
        step = 4
        end = 3
        while i <= self.info_num:
            record_type = struct.unpack(BYTE_ORDER + 'B', data[3 + i * step : 6 + i * step])
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

    def unpack_sq1(self, data):
        i = 0
        step = 7
        end = 0
        while i <= self.info_num:
            ia = self.get_info_addr(data[0 + i * step : 3 + i + step])
            self.info_addrs.append(ia)
            value = data[3 + i * step : 6 + i * step]
            info = struct.unpack(BYTE_ORDER + 'B', data[6 + i * step : 7 + i * step])
            end = 7 + i * step
            self.infos.append(info)
            i = i + 1
        return data[end:]

class CDSCSJ(BaseCMD):
    def unpack(self, data):
        self.CDSCDY = struct.unpack(BYTE_ORDER + 'H', data[0:2])
        self.CDSCDL = struct.unpack(BYTE_ORDER + 'H', data[2:4])
        self.SCJDQZT = struct.unpack(BYTE_ORDER + 'B', data[4:5])
        self.LJQRKGZT = struct.unpack(BYTE_ORDER + 'B', data[5:6])
        self.YGZDD = struct.unpack(BYTE_ORDER + 'L', data[6:10])
        self.CDZBH = data[10:18]
        self.SFLJDC = struct.unpack(BYTE_ORDER + 'B', data[10:11])
        self.GZZT = struct.unpack(BYTE_ORDER + 'H', data[11:13])
        self.CDQBH = struct.unpack(BYTE_ORDER + 'B', data[13:14])
        self.CDQLX = struct.unpack(BYTE_ORDER + 'B', data[14:15])
        self.GZYYDM = struct.unpack(BYTE_ORDER + 'B', data[15:16])
        return data[16:]

class JQSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.LJKH = data[8:16]
        self.KMM = data[16:32]
        self.SRMM = data[32:48]
        self.KYE = struct.unpack(BYTE_ORDER + 'I', data[48:52])
        self.KZT = struct.unpack(BYTE_ORDER + 'H', data[52:54])
        self.DDQCWYBS = data[54:86]
        self.JFMXBM = data[86:94]
        self.DDCCPHM = data[94:112]
        self.CDQBH = struct.unpack(BYTE_ORDER + 'B', data[112:113])
        self.SJJYY = data[113:129]
        return data[129:]

class TZCDSJ(BaseCMD):
    def unpack(self, data):
        self.JYLSH = data[0:16]
        self.YWLX = data[16:18]
        self.ZDJQBM = data[18:26]
        self.YHBH = data[26:32]
        self.LJKH = data[32:40]
        self.KSSJ = data[40:47]
        self.JSSJ = data[47:54]
        self.JQSZ = data[54:58]
        self.JZSZ = data[58:62]
        self.FQSZ = data[64:66]
        self.FZSZ = data[66:70]
        self.PQSZ = data[70:74]
        self.PZSZ = data[74:78]
        self.GQSZ = data[78:82]
        self.GZSZ = data[82:86]
        self.JDL = data[86:90]
        self.FDL = data[90:94]
        self.PDL = data[94:98]
        self.GDL = data[98:102]
        self.ZDL = data[102:106]
        self.JLSSLX = data[106:108]
        self.BCJLSS = data[108:112]
        self.SCJLSS = data[112:116]
        self.SCCHDZBH = data[116:121]
        self.SCYWLX = data[121:123]
        self.DDQCWYBS = data[123:155]
        self.JGE = data[155:159]
        self.FJE = data[159:163]
        self.PJE = data[163:167]
        self.GJE = data[167:171]
        self.ZJE = data[171:175]
        self.DDCCPHM = data[175:193]
        self.CDQBH = data[193:194]
        self.YYLSH = data[194:214]
        self.SJJYY = data[214:230]
        return data[230:]

class SCJYSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.JYLSH = data[8:24]
        self.YHBH = data[24:32]
        self.LJKH = data[32:40]
        self.LXJYLX = data[40:41]
        self.KSSJ = data[41:48]
        self.JSSJ = data[48:55]
        self.JQSZ = data[55:59]
        self.JZSJ = data[59:63]
        self.FQSZ = data[63:67]
        self.FZSZ = data[67:71]
        self.PQSZ = data[71:76]
        self.PZSZ = data[76:80]
        self.GQSZ = data[80:84]
        self.GZSZ = data[84:88]
        self.JLLX = data[88:90]
        self.BCJLSS = data[90:94]
        self.SCJLSS = data[94:98]
        self.GDL = data[98:102]
        self.GGE = data[102:106]
        self.FDL = data[106:110]
        self.FJE = data[110:114]
        self.PDL = data[114:118]
        self.PJE = data[118:122]
        self.GDL = data[122:126]
        self.GJE = data[126:130]
        self.ZDL = data[130:134]
        self.YWLX = data[134:136]
        self.XFSZ = data[136:140]
        self.XFDJ = data[140:144]
        self.XFJE = data[144:148]
        self.DDQCWYBS = data[148:180]
        self.DDCCPHM = data[180:198]
        self.CDQBH = data[198:199]
        self.SJJYY = data[199:215]
        return data[215:]

class HMDXFSJ(BaseCMD):
    def unpack(self, data):
        self.LJKH = data[0:8]
        self.ZT = data[8:10]
        self.ZHGXSJ = data[10:17]
        self.DDCCPHM = data[17:35]
        return data[35:]

class XFBZFLSJ(BaseCMD):
    def unpack(self, data):
        self.SXSJ = data[0:7]
        self.SXSJ = data[7:14]
        self.ZXZT = data[14:16]
        self.JLLX = data[16:18]
        self.JDJ = data[18:22]
        self.FDJ = data[22:26]
        self.PDJ = data[26:30]
        self.GDJ = data[30:34]
        return data[34:]

class JQXXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.LJKH = data[8:16]
        self.DDQCWYBS = data[16:48]
        self.JFMXBM = data[48:56]
        self.KKHKYE = data[56:60]
        self.JQCGBZ = data[60:61]
        self.JQSBYY = data[61:63]
        self.SYLC = data[63:67]
        self.SYDL = data[67:71]
        self.SYCS = data[71:75]
        self.DDCCPHM = data[75:93]
        self.CDQBH = data[93:94]
        self.YYBH = data[94:104]
        self.SJJYY = data[104:114]
        return data[114:]

class KKHXXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.LJKH = data[8:16]
        self.KKJE = data[16:20]
        self.ZHYE = data[20:24]
        self.KKCGBZ = data[24:25]
        self.KKSBYY = data[25:27]
        self.KCLC = data[27:31]
        self.SYLC = data[31:35]
        self.KCDL = data[35:39]
        self.SYDL = data[39:43]
        self.KCCS = data[43:47]
        self.SYCS = data[47:51]
        self.DDCCPHM = data[51:69]
        self.CDQBH = data[69:70]
        self.SJJYY = data[70:76]
        return data[76:]

class CSSJ(BaseCMD):
    def unpack(self, data):
        self.CSDM = data[0:2]
        self.CSZCD = data[2:3]
        self.CSZ = data[3:67]
        return data[67:]

class FDDLSDSZ(BaseCMD):
    def unpack(self, data):
        self.JDLKSSJ1 = data[0:2]
        self.JDLJSSJ1 = data[2:4]
        self.JDLKSSJ2 = data[4:6]
        self.JDLJSSJ2 = data[6:8]
        self.FDLKSSJ1 = data[8:10]
        self.FDLJSSJ1 = data[10:12]
        self.FDLKSSJ2 = data[12:14]
        self.FDLJSSJ2 = data[14:16]
        self.PDLKSSJ1 = data[16:18]
        self.PDLJSSJ1 = data[18:20]
        self.PDLKSSJ2 = data[20:22]
        self.PDLJSSJ2 = data[22:24]
        self.GDLKSSJ1 = data[24:26]
        self.GDLJSSJ1 = data[26:28]
        self.GDLKSSJ2 = data[28:30]
        self.GDLJSSJ2 = data[30:32]
        return data[32:]

class CDYYXXSJ(BaseCMD):
    def unpack(self, data):
        self.JYLSH = data[0:10]
        self.ZDJQBM = data[10:18]
        self.YHKH = data[18:26]
        self.CPHM = data[26:44]
        self.CDLX = data[44:45]
        self.CDQBH = data[45:46]
        self.YYKSSJ = data[46:53]
        self.YYCDCL = data[53:55]
        self.YYCDCS = data[55:57]
        return data[57:]

class CDYYSXSJ(BaseCMD):
    def unpack(self, data):
        self.JYLSH = data[0:10]
        self.ZDJQBM = data[10:18]
        self.YHKH = data[18:26]
        self.CPHM = data[26:44]
        self.CDLX = data[44:45]
        self.CDQBH = data[45:46]
        self.YYKSSJ = data[46:53]
        self.YYCDCL = data[53:55]
        self.YYCDCS = data[55:57]
        self.YYJG = data[57:59]
        return data[59:]

class QXYYXXSJ(BaseCMD):
    def unpack(self, data):
        self.JYLSH = data[0:10]
        self.ZDJQBM = data[10:18]
        self.YHKH = data[18:26]
        self.CPHM = data[26:44]
        self.CDLX = data[44:45]
        self.CDQBH = data[45:46]
        self.YYKSSJ = data[46:53]
        self.YYCDCL = data[53:55]
        self.YYCDCS = data[55:57]
        return data[57:]

class QXYYSXSJ(BaseCMD):
    def unpack(self, data):
        self.JYLSH = data[0:10]
        self.ZDJQBM = data[10:18]
        self.YHKH = data[18:26]
        self.CPHM = data[26:44]
        self.CDLX = data[44:45]
        self.CDQBH = data[45:46]
        self.YYKSSJ = data[46:53]
        self.YYCDCL = data[53:55]
        self.YYCDCS = data[55:57]
        self.QXJG = data[57:59]
        return data[59:]

class YYCXXXSJ(BaseCMD):
    def unpack(self, data):
        self.JYLSH = data[0:10]
        self.ZDJQBM = data[10:18]
        self.YHKH = data[18:26]
        self.CPHM = data[26:44]
        self.YYKSSJ = data[44:51]
        return data[51:]

class YYCXSXSJ(BaseCMD):
    def unpack(self, data):
        self.JYLSH = data[0:10]
        self.ZDJQBM = data[10:18]
        self.YHKH = data[18:26]
        self.CPHM = data[26:44]
        self.CDLX = data[44:45]
        self.CDQBH = data[45:46]
        self.YYKSSJ = data[46:53]
        self.YYCDCL = data[53:55]
        self.YYCDCS = data[55:57]
        self.CXJG = data[57:59]
        return data[59:]


class JHCDSXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.LJKH = data[8:16]
        self.DDCCPHM = data[16:34]
        self.CDLX = data[34:35]
        self.CDQBH = data[35:36]
        self.JRCDZTCGBZ = data[36:37]
        self.JRCDZTCGBZSBYY = data[37:39]
        return data[39:]

class RJSJJHXXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.RJBB = data[8:10]
        self.DWJDX = data[10:14]
        self.GWJDX = data[14:18]
        self.DWJJYM = data[18:50]
        self.GWJJYM = data[50:82]
        self.WJDM = data[82:114]
        self.WJMC = data[114:178]
        return data[178:]

class RJSJJHSXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.RJBB = data[8:10]
        self.WJDM = data[10:42]
        return data[42:]

class DZRJSJSXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.RJBB = data[8:10]
        self.WJDM = data[10:42]
        self.GDWBJ = data[42:43]
        self.PYL = data[43:47]
        self.length = data[47:51]
        return data[51:]

class RJSJXXYDSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.PYL = data[8:12]
        self.WJNRCD = data[12:16]
        self.DATA = data[16:16 + self.WJNRCD]
        self.CRC = data[16 + self.WJNRCD:16 + self.WJNRCD + 2]
        return data[16 + self.WJNRCD + 2:]

class GZMSQHXXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.GZMS = data[8:10]
        return data[10:]

class GZMSQHSXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.GZMS = data[8:10]
        self.MSQHJG = data[10:12]
        return data[12:]

class GZMSCXXXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        return data[8:]

class GZMSCXSXSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.GZMS = data[8:10]
        return data[10:]

class ZDSBSJ(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.XXDM = data[8:9]
        self.CDQBH = data[9:10]
        return data[10:]

class ZXXFJS(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.YHKH = data[8:16]
        self.XXDM = data[16:17]
        self.CDQBH = data[17:18]
        return data[18:]

class ZXQZJS(BaseCMD):
    def unpack(self, data):
        self.ZDJQBM = data[0:8]
        self.YHKH = data[8:16]
        self.XXDM = data[16:17]
        self.CDQBH = data[17:18]
        return data[18:]


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
        _len = struct.unpack('B', stream[1])
        _rlen = _len - 2 #去除0x68头和长度所占位置
        pkg = stream[0:_len]
        apdu = APDU() 
        data = apdu.unpack(pkg)
        return True, apdu, stream[_len:]

    def encode(self, cmd_data):
        pkg = ''
        apdu = APDU()
        pkg = apdu.pack()
        return pkg

