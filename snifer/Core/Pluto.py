#-*- coding:utf-8 -*-
from .BaseType import *
from .Plutos import *

class MSGType:
	LOGINAPP = 1 << 12
	

class MSGID:
	#服务器发给客户端的包
	MSGID_CLIENT_LOGIN_RESP = 1                                  #//服务器发给客户端的账号登录结果
	MSGID_CLIENT_NOTIFY_ATTACH_BASEAPP = 2                                  #//连接baseapp通知
	MSGID_CLIENT_ENTITY_ATTACHED = 3                                  #//通知客户端已经attach到一个服务器entity,同时刷数据
	MSGID_CLIENT_AVATAR_ATTRI_SYNC = 4                                  #//AVATAR相关属性修改同步
	MSGID_CLIENT_RPC_RESP = 5                                  #//服务器发给客户端的rpc
	MSGID_CLIENT_ENTITY_POS_SYNC = 6                                 #//服务器告诉客户端坐标变化(move)
	CLIENT_ENTITY_SPACE_CHANGE        = 7                                  #//服务器告诉客户端场景变化
	MSGID_CLIENT_AOI_ENTITIES = 8                                   #//服务器告诉客户端aoi范围内的entity
	MSGID_CLIENT_AOI_NEW_ENTITY = 9                                   #//服务器告诉客户端aoi范围内新增的entity
	MSGID_CLIENT_ENTITY_CELL_ATTACHED = 10                                  #//服务器打包给客户端的cell_client属性
	MSGID_CLIENT_OTHER_ENTITY_ATTRI_SYNC = 11 								  #//其他entity属性变化同步
	MSGID_CLIENT_OTHER_ENTITY_POS_SYNC = 12 								  #//其他entity坐标变化同步(move)
	CLIENT_OTHER_ENTITY_MOVE_REQ = 13                                  #//服务器转发的其他entity的移动请求
	CLIENT_OTHER_RPC_RESP             = 14                                  #//对其他客户端entity的rpc
	MSGID_CLIENT_AOI_DEL_ENTITY = 15                                  #//有entity离开了aoi
	
	CLIENT_ENTITY_POS_PULL = 16                                  #//服务器告诉客户端坐标变化(拉扯)
	CLIENT_OTHER_ENTITY_POS_PULL = 17                                  #//服务器转发的其他entity的移动请求(拉扯)
	MSGID_CLIENT_ENTITY_POS_TELEPORT = 18                                 #//服务器告诉客户端坐标变化(teleport)
	CLIENT_OTHER_ENTITY_TELEPORT = 19                                  #//服务器转发的其他entity的移动请求(teleport)
	
	CLIENT_CHECK_RESP = 20                                #//客户端发给服务器的包
	MSGID_CLIENT_RELOGIN_RESP = 21                      #//服务端拒绝断线重连
	MSGID_CLIENT_NOTIFY_MULTILOGIN = 22                         #//服务端拒绝连接
	
	LOGINAPP_CHECK = 30                                   #//客户端版本校验
	
	#客户端发给服务器的包
	MSGID_LOGINAPP_LOGIN = 31                                  #//客户端输入帐户名/密码进行登录验证
	BASEAPP_CLIENT_LOGIN = 32 
	BASEAPP_CLIENT_RPCCALL = 33                                  #//客户端发起的远程调用
	MSGID_BASEAPP_CLIENT_MOVE_REQ = 34                                  #//客户端发起的移动
	BASEAPP_CLIENT_RPC2CELL_VIA_BASE = 35                           #//客户端cell远程调用
	MSGID_BASEAPP_CLIENT_OTHERS_MOVE_REQ = 36                           #//客户端cell远程调用
	MSGID_BASEAPP_CLIENT_RELOGIN = 37                                     #//客户端发起断线重连
	
	#暂定50以下的是客户端和服务器的交互包 需要加密
	MAX_CLIENT_MSGID = 50 
	
	ALLAPP_ONTICK = 101                                 #//心跳消息
	ALLAPP_SETTIME = 102                                 #//同步时间消息
	ALLAPP_SHUTDOWN_SERVER = 103                                 #//关闭服务器通知
	
	LOGINAPP_LOGIN                    = MSGType.LOGINAPP + 1                #//客户端输入帐户名/密码进行登录验证
	LOGINAPP_MODIFY_LOGIN_FLAG = MSGType.LOGINAPP + 6               #//修改服务器是否可以登录标记
	LOGINAPP_SELECT_ACCOUNT_CALLBACK = MSGType.LOGINAPP + 7 
	LOGINAPP_NOTIFY_CLIENT_TO_ATTACH = MSGType.LOGINAPP + 8 

class BitCryto:
	crytoKey = []
	offsetOfKey = 0
	
	def __init__(self, sKey):
	    self.crytoKey = sKey
	
	def Encode(self, inputByte):
	    if (self.offsetOfKey >= len(self.crytoKey)):
	        self.offsetOfKey = 0
	    offset = self.crytoKey[self.offsetOfKey]
	    self.offsetOfKey = self.offsetOfKey + 1
	
	    outputByte = ((offset + inputByte) & 0xff)
	    return outputByte
	
	def Decode(self, inputByte):
	    if (self.offsetOfKey >= len(self.crytoKey)):
	        self.offsetOfKey = 0
	    offset = self.crytoKey[self.offsetOfKey]
	    self.offsetOfKey = self.offsetOfKey + 1
	
	    outputByte = inputByte - offset
	    if (outputByte < 0):
	        outputByte = outputByte + 256
	    return struct.pack('B', outputByte)
	
	def Reset(self, startOffset = 0):
	    if (startOffset == 0):
	        self.offsetOfKey = 0
	    else:
	        self.offsetOfKey = (startOffset % len(self.crytoKey))

class Pluto:
	decode_type = ''
	def __init__(self):
		self.cryto = BitCryto([0, 0])

	def decode(self, data):
		nidx, msg_id = BaseTypeParse.parse_uint16(data, 0)
		self.cryto.Reset()
		i = nidx
		ndata = data[:i]
		while i < len(data):
			#data[i] = self.cryto.Decode(data[i])
			ndata = ndata + self.cryto.Decode(data[i])
			i = i + 1
		#print("msg_id ", msg_id, ndata)
		pluto = None
		if msg_id == MSGID.MSGID_CLIENT_RPC_RESP:
			pluto = RpcCallPluto();
			pluto.decode_client(ndata, nidx)
		elif msg_id == MSGID.BASEAPP_CLIENT_RPCCALL:
			pluto = RpcCallPluto()
			pluto.decode_svr(ndata, nidx, 33)
		elif msg_id == MSGID.BASEAPP_CLIENT_RPC2CELL_VIA_BASE:
			pluto = RpcCallPluto()
			pluto.decode_svr(ndata, nidx, 35)
		else:
			print('msg_id', msg_id, ndata)
		#elif msg_id ==  MSGID.MSGID_CLIENT_LOGIN_RESP:
		#	pluto = LoginPluto.Create();
		#elif msg_id ==  MSGID.MSGID_CLIENT_NOTIFY_ATTACH_BASEAPP:
		#	pluto = BaseLoginPluto.Create();
		#elif msg_id ==  MSGID.MSGID_CLIENT_ENTITY_ATTACHED:
		#	pluto = EntityAttachedPluto.Create();
		#elif msg_id ==  MSGID.MSGID_CLIENT_AOI_NEW_ENTITY:
		#	pluto = AOINewEntityPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_AOI_DEL_ENTITY:
		#	pluto = AOIDelEntityPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_OTHER_ENTITY_POS_SYNC:
		#	pluto = OtherEntityPosSyncPluto.Create();
		#elif msg_id == MSGID.CLIENT_OTHER_ENTITY_POS_PULL:
		#	pluto = OtherEntityPosPullPluto.Create();
		#elif msg_id == MSGID.CLIENT_OTHER_ENTITY_TELEPORT:
		#	pluto = OtherEntityPosTeleportPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_ENTITY_CELL_ATTACHED:
		#	pluto = EntityCellAttachedPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_AOI_ENTITIES:
		#	pluto = AOIEntitiesPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_AVATAR_ATTRI_SYNC:
		#	pluto = AvatarAttriSyncPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_OTHER_ENTITY_ATTRI_SYNC:
		#	pluto = OtherAttriSyncPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_ENTITY_POS_SYNC:
		#	pluto = EntityPosSyncPluto.Create();
		#elif msg_id == MSGID.CLIENT_ENTITY_POS_PULL:
		#	pluto = EntityPosPullPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_ENTITY_POS_TELEPORT:
		#	pluto = EntityPosTeleportPluto.Create();
		#elif msg_id == MSGID.CLIENT_CHECK_RESP:
		#	pluto = CheckDefMD5Pluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_RELOGIN_RESP:
		#	pluto = ReConnectPluto.Create();
		#elif msg_id == MSGID.MSGID_CLIENT_NOTIFY_MULTILOGIN:
		#	pluto = DefuseLoginPluto.Create();
		#else:
		#	print("unsuport msg_id " + msg_id)
			
