#-*- coding:utf-8 -*-
from . import *

class BaseTypeParse:
	def __init__(BaseTypeParse):
		pass

	@staticmethod
	def parse_int8(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'b', data[start_idx:start_idx + 1])[0]
		return start_idx + 1, rst

	@staticmethod
	def parse_uint8(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'B', data[start_idx:start_idx + 1])[0]
		return start_idx + 1, rst

	@staticmethod
	def parse_int16(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'h', data[start_idx:start_idx + 2])[0]
		return start_idx + 2, rst

	@staticmethod
	def parse_uint16(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'H', data[start_idx:start_idx + 2])[0]
		return start_idx + 2, rst

	@staticmethod
	def parse_int32(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'i', data[start_idx:start_idx + 4])[0]
		return start_idx + 4, rst

	@staticmethod
	def parse_uint32(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'I', data[start_idx:start_idx + 4])[0]
		return start_idx + 4, rst

	@staticmethod
	def parse_int64(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'q', data[start_idx:start_idx + 8])[0]
		return start_idx + 8, rst

	@staticmethod
	def parse_uint64(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'Q', data[start_idx:start_idx + 8])[0]
		return start_idx + 8, rst

	@staticmethod
	def parse_float(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'f', data[start_idx:start_idx + 4])[0]
		return start_idx + 4, rst

	@staticmethod
	def parse_double(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + 'd', data[start_idx:start_idx + 8])[0]
		return start_idx + 8, rst

	@staticmethod
	def parse_bool(data, start_idx):
		rst = struct.unpack(BYTE_ORDER + '?', data[start_idx:start_idx + 1])[0]
		return start_idx + 1, rst

	@staticmethod
	def parse_blob(data, start_idx):
		nidx, dlen = BaseTypeParse.parse_uint16(data, start_idx)
		rst = data[nidx:nidx + dlen]
		return nidx + dlen, rst

	@staticmethod
	def parse_luatable(data, start_idx):
		nidx, dlen = BaseTypeParse.parse_uint16(data, start_idx)
		rst = data[nidx:nidx + dlen]
		return nidx + dlen, rst

	@staticmethod
	def parse_string(data, start_idx):
		nidx, dlen = BaseTypeParse.parse_uint16(data, start_idx)
		rst = data[nidx:nidx + dlen]
		return nidx + dlen, rst

	@staticmethod
	def parse(t, data, start_idx):
		if t == "STRING":
			return BaseTypeParse.parse_string(data, start_idx)
		elif t == "INT8":
			return BaseTypeParse.parse_int8(data, start_idx)
		elif t == "UINT8":
			return BaseTypeParse.parse_uint8(data, start_idx)
		elif t == "INT16":
			return BaseTypeParse.parse_int16(data, start_idx)
		elif t == "UINT16":
			return BaseTypeParse.parse_uint16(data, start_idx)
		elif t == "INT32":
			return BaseTypeParse.parse_int32(data, start_idx)
		elif t == "UINT32":
			return BaseTypeParse.parse_uint32(data, start_idx)
		elif t == "INT64":
			return BaseTypeParse.parse_int64(data, start_idx)
		elif t == "UINT64":
			return BaseTypeParse.parse_uint64(data, start_idx)
		elif t == "FLOAT":
			return BaseTypeParse.parse_float(data, start_idx)
		elif t == "FLOAT64":
			return BaseTypeParse.parse_double(data, start_idx)
		elif t == "BOOL":
			return BaseTypeParse.parse_bool(data, start_idx)
		elif t == "PB_BLOB" or t == "BLOB":
			return BaseTypeParse.parse_blob(data, start_idx)
		elif t == "LUA_TABLE":
			return BaseTypeParse.parse_luatable(data, start_idx)
		else:
			print('unsuport type ' + t)
			return (0, 0)
