#-*- coding:utf-8 -*-
class DataCenter:
		def __init__(self):
				self.datas = {}
				
		def register(self, data_name, data):
				self.datas[data_name] = data
				
		def get_data(self, data_name):
				return self.datas.get(data_name, None)