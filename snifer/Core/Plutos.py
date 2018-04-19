#-*- coding:utf-8 -*-
from .BaseType import BaseTypeParse
from .EntityDef import EntityDef
#decode_client for client parse server data

#decode_svr for server parse client data
class AOIDelEntityPluto:

	def decode_client(self, data, idx):
		nidx, self.entity = BaseTypeParse.parse_uint32(data, idx)
		print(self.__name__ + "  " + self.entity)
		return nidx, self.entity

	def decode_svr(self, data, idx):
		return idx, 0

class AOIEntitiesPluto:
	def decode_client(self, data, idx):
		nidx, type_id = BaseTypeParse.parse_uint16(data, idx)
		nidx, eid = BaseTypeParse.parse_uint32(data, nidx)
		nidx, angle_x = BaseTypeParse.parse_uint8(data, nidx)
		nidx, angle_y = BaseTypeParse.parse_uint8(data, nidx)
		nidx, angle_z = BaseTypeParse.parse_uint8(data, nidx)
		nidx, x = BaseTypeParse.parse_int32(data, nidx)
		nidx, y = BaseTypeParse.parse_int32(data, nidx)
		nidx, z = BaseTypeParse.parse_int32(data, nidx)
		while nidx < len(data):
			nidx, elen = BaseTypeParse.parse_uint16(data, nidx)
			end = nidx + elen
			nidx, tid = BaseTypeParse.parse_uint16(data, nidx)
			nidx, eid = BaseTypeParse.parse_uint32(data, nidx)
			nidx, angle_x = BaseTypeParse.parse_uint8(data, nidx)
			nidx, angle_y = BaseTypeParse.parse_uint8(data, nidx)
			nidx, angle_z = BaseTypeParse.parse_uint8(data, nidx)
			nidx, x = BaseTypeParse.parse_int32(data, nidx)
			nidx, y = BaseTypeParse.parse_int32(data, nidx)
			nidx, z = BaseTypeParse.parse_int32(data, nidx)
			edef = EntityDef.defs[tid]
			if not edef:
				continue
			while nidx < end:
				nidx, idx = BaseTypeParse.parse_uint16(data, nidx)
				p = edef.props[idx]
				t = p.type_name
				nidx, rst = BaseTypeParse.parse(t, data, nidx)
		return nidx, 0

	def decode_svr(self, data, idx):
		return idx, 0

class AOINewEntityPluto:
	def decode_client(self, data, idx):
		nidx, tid = BaseTypeParse.parse_uint16(data, idx)
		nidx, eid = BaseTypeParse.parse_uint32(data, nidx)
		nidx, angle_x = BaseTypeParse.parse_uint8(data, nidx)
		nidx, angle_y = BaseTypeParse.parse_uint8(data, nidx)
		nidx, angle_z = BaseTypeParse.parse_uint8(data, nidx)
		nidx, x = BaseTypeParse.parse_int32(data, nidx)
		nidx, y = BaseTypeParse.parse_int32(data, nidx)
		nidx, z = BaseTypeParse.parse_int32(data, nidx)
		edef = EntityDef.desf[tid]
		if not edef:
			return
		while nidx < len(data):
			nidx, idx = BaseTypeParse.parse_uint16(data, nidx)
			p = edef.props[idx]
			t = p.type_name
			nidx, rst = BaseTypeParse.parse(t, data, nidx)
		return nidx, 0

	def decode_svr(self, data, idx):
		return idx, 0

class AvatarAttriSyncPluto:
	def decode_client(self, data, idx):
		pass

class RpcCallPluto:
	def decode_client(self, data, idx):
		nidx, func_id = BaseTypeParse.parse_uint16(data, idx)
		edef = EntityDef.default
		method = edef.client_methods.get(func_id, None)
		if not method:
			print("unsuport client method id", func_id)
			return
		args = []
		for arg in method.args:
			nidx, value = BaseTypeParse.parse(arg, data, nidx)
			args.append(value)
		print("server call client method ", method.func_name, args)

	def decode_svr(self, data, idx, borc=0):
		#nidx, borc = BaseTypeParse.parse_uint16(data, idx)
		nidx, func_id = BaseTypeParse.parse_uint16(data, idx)
		edef = EntityDef.default
		methods = {}
		rpctype = ''
		if borc == 35: #BASEAPP_CLIENT_RPC2CELL_VIA_BASE
			rpctype = 'cell'
			methods = edef.cell_methods
		elif borc == 33: #BASEAPP_CLIENT_RPCCALL
			rpctype = 'base'
			methods = edef.base_methods
		else:
			print("unsuport base or cell rpc type", borc)
			return
		method = methods.get(func_id, None)
		if not method:
			print("unsuport svr method id", func_id)
			return
		args = []
		for arg in method.args:
			nidx, value = BaseTypeParse.parse(arg, data, nidx)
			args.append(value)
		print("client call ", rpctype, " method", method.func_name, args)
		
