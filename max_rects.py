#-*- coding:utf-8 -*-
import dircache, os, math
from PIL import Image
from psd_tools import PSDImage
from psd_tools import Group
import json

class Rect:
	width = 0
	height = 0
	x = 0
	y = 0
	name = ""

class MergeImg:
	sizes = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
	div = 1 #间隔像素
	width = 0
	height = 0
	imgs = []
	total_arena = 0
	
	def __init__(self):
		pass
		
	def set_imgs(self, imgs):
		self.imgs = imgs
		
	def caculate_arena(self):
		for img in self.imgs:
			w, h = img.width, img.height
			self.total_arena = self.total_arena + w * h
		print "total_arena " + self.total_arena
		
	def get_max_arena(self):
		arena = 0
		rst = None
		for rect in self.imgs:
			a = rect.width * rect.height
			if a > arena:
				arena = a
				rst = rect
		return rst
		
	def get_max_width(self):
		w = 0
		rst = None
		for rect in self.imgs:
			a = rect.width
			if a > w:
				w = a
				rst = rect
		return rst
		
	def get_max_height(self):
		h = 0
		rst = None
		for rect in self.imgs:
			a = rect.height
			if a > h:
				h = a
				rst = rect
		return rst
		
	def merge(self):
		w = math.sqrt(self.total_arena)
		for i in self.sizes:
			if i >= w:
				w = i
				break
		

class MergeTool:
	#原图目录
	res_path = "E:/Temp/abc"
	#生成的图集存放目录
	output_path = "E:/Temp"
	cells = []
	total_arena = 0
	MAX_ARENA = 2048 * 2048
	
	def __init__(self):
		pass
		
	def begin(self):
		files = dircache.listdir(self.res_path)
		for f in files:
			p = self.res_path + '/' + f
			img = Image.open(p)
			self.cells.append(img)
			img_width, img_height = img.size
			self.total_arena = self.total_arena + img_width * img_height
		print self.total_arena

if __name__ == "__main__":
	d = MergeTool()
	d.begin()