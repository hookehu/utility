#-*- coding:utf-8 -*-
import dircache, os, math
from PIL import Image
from psd_tools import PSDImage
from psd_tools import Group
import json

class SplitTool:
	#原图目录
	res_path = "E:/pathto/scence"
	output_path = "E:/output"
	#生成的小图存放目录
	output_path = "E:/pathto/auto_scene_split"
	#JPEG格式切分的尺寸
	jpg_width = 720.0
	jpg_height = 1280.0
	#JPEG压缩品质
	jpg_quality = 70
	#PNG格式切分的尺寸
	png_width = 200.0
	png_height = 200.0
	sheets = {} #{filename:{gridname:[x,y], ...}, ...}
	
	def __init__(self):
		print "SplitTool"
		pass
		
	def begin(self):
		files = dircache.listdir(self.res_path)
		print files
		for f in files:
			#if f != 'map_30001.jpg':
				#continue
			p = self.res_path + '/' + f
			self.split_one(p, f)
		file = self.output_path + '/map_sheets.json'
		jsonstr = json.dumps(self.sheets, indent = 4, encoding="utf-8")
		fd = open(file, 'wb')
		fd.write(jsonstr);
		fd.close();
		
	def split_one(self, longname, file):
		if file.find('.jpg') > 0:
			self.split_jpg(longname, file)
		elif file.find('.png') > 0:
			self.split_png(longname, file)
		else:
			print 'error'
			
	def split_jpg(self, longname, file):
		name = file.split('.')[0]
		img = Image.open(longname)
		img_width, img_height = img.size
		col = int(math.ceil(img_width / self.jpg_width))
		row = int(math.ceil(img_height / self.jpg_height))
		sheet = {}
		for r in xrange(row):
			y = r * self.jpg_height
			for c in xrange(col):
				x = c * self.jpg_width
				w = self.jpg_width
				h = self.jpg_height
				if x + w > img_width:
					w = img_width - x
				if y + h > img_height:
					h = img_height - y
				w = int(w)
				h = int(h)
				#new_img = Image.new(img.mode, (w, h))
				x1 = x + w
				y1 = y + h
				new_img = img.crop((x, y, x1, y1))
				new_img_name = self.output_path + '/' + name + '_' + str(r * col + c) + '.jpg'
				new_img.save(new_img_name, quality=self.jpg_quality)
				n = name + '_' + str(r * col + c) + '_jpg'
				sheet[n] = (x, y)
		self.sheets[name + '_jpg'] = sheet
		
	def split_png(self, longname, file):
		#print file
		name = file.split('.')[0]
		img = Image.open(longname)
		img_width, img_height = img.size
		col = int(math.ceil(img_width / self.png_width))
		row = int(math.ceil(img_height / self.png_height))
		sheet = {}
		for r in xrange(row):
			y = r * self.png_height
			for c in xrange(col):
				x = c * self.png_width
				w = self.png_width
				h = self.png_height
				if x + w > img_width:
					w = img_width - x
				if y + h > img_height:
					h = img_height - y
				w = int(w)
				h = int(h)
				x1 = x + w
				y1 = y + h
				new_img = img.crop((x, y, x1, y1))
				new_img_name = self.output_path + '/' + name + '_' + str(r * col + c) + '.png'
				new_img.save(new_img_name)
				n = name + '_' + str(r * col + c) + '_png'
				sheet[n] = (x, y)
		self.sheets[name + '_png'] = sheet

def test():
	im = PSDImage.load("D:\\a.psd")
	print dir(im)
	print im.layers
	for layer in im.layers:
		#print dir(layer)
		if type(layer) is Group:
			printgroup(layer)
		else:
			print layer.name.encode("gb2312")
		#print layer.name.encode("gb2312")
		
def printgroup(group):
	for layer in group.layers:
		if type(layer) is Group:
			printgroup(layer)
		else:
			print layer.name.encode("gb2312") + str(layer.bbox)

if __name__ == "__main__":
	d = SplitTool()
	d.begin()
