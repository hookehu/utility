#-*- coding:utf-8 -*-
import os
import sys
import pcap
import dpkt
import struct
import xml.etree.ElementTree as ET

from Core import Pluto, EntityDef

class Sniffer:
	
	def __init__(self, default = '', t = 'c', f=''):
		self.default = default
		self.data = b""
		self.pkgs = []
		self.pluto = Pluto.Pluto()
		self.init_defs()
		Pluto.Pluto.decode_type = t
		self.filter_str = f

	def init_defs(self):
		parent_path = os.path.dirname(__file__)
		if parent_path == "":
			parent_path = '.'
		xml = ET.parse(parent_path + "/entity_defs/entities.xml")
		root = xml.getroot()
		i = 0
		for node in root:
			name = node.tag
			x = ET.parse(parent_path + "/entity_defs/" + name + ".xml")
			r = x.getroot()
			entity_def = EntityDef.EntityDef()
			entity_def.parse(r)
			EntityDef.EntityDef.defs[i] = entity_def
			if name == self.default:
				EntityDef.EntityDef.default = entity_def
			i = i + 1
		print(len(EntityDef.EntityDef.defs))
			

	def proc(self):
		cap = pcap.pcap()
		cap.setfilter(self.filter_str)
		for t, data in cap:
			#print(data)
			eth = dpkt.ethernet.Ethernet(data)
			if eth.data.__class__.__name__ != 'IP':
				continue
			if eth.data.data.__class__.__name__ != 'TCP':
				continue
			#print(eth.data.data.data)
			self.data = self.data + eth.data.data.data
			self.dopkg()
			

	def dopkg(self):
		#4byte head + 2byte + 2byte msg_id + body
		if len(self.data) < 4: # < header len
			return
		pkgLen = struct.unpack('>I', self.data[0:4])[0]
		msgLen = pkgLen - 4 - 2
		if len(self.data) < pkgLen:
			return
		pkg = self.data[:pkgLen]
		self.pluto.decode(pkg[6:])
		self.data = self.data[pkgLen:]
		
if __name__ == "__main__":
	print(sys.argv)
	def_name = sys.argv[1]
	t = sys.argv[2]
	f = sys.argv[3:]
	fs = ' '.join(f)
	print(fs)
	s = Sniffer(def_name, t, fs)
	#print(dir(dpkt.tcp))
	s.proc()
	print("success")
