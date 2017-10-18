#-*- coding:utf-8 -*-
import os
from selenium import webdriver
from time import sleep

class EXML2JS:
		path = "http://url/index.html"
		input_path = "E:/url/panels"
		output_path = "E:/urls/"
		new_js = '''function t(text)
								{
										var p = new eui.sys.EXMLParser();
										var doc = egret.XML.parse(text);
										delete doc.attributes["class"];
										var cc = p.parseClass(doc, "classname");
										var rst = cc.toCode();
										return rst;
								};''';
		jj = '''return eui;'''
		count = 0

		def __init__(self):
				#print dir(webdriver)
				#self.driver = webdriver.PhantomJS()
				self.driver = webdriver.Chrome()
				#self.driver = webdriver.Firefox()
				self.driver.set_window_size(1280, 720)
				self.driver.get(self.path)
				print dir(self.driver)
				self.test()
				
		def proc(self):
				#self.convert_folder(self.input_path)
				self.driver.quit()
				pass
				
		def convert_folder(self, path):
				files = os.listdir(path)
				for	file in	files:
						p	=	path	+	'/'	+	file
						if os.path.isdir(p):
								self.convert_folder(p)
						else:
								self.convert_file(p)
								
		def convert_file(self, path):
				self.count = self.count + 1
				#print path
				fd = open(path, "rb")
				content = fd.read()
				fd.close()
				content = content.replace('\n', "").replace('\r', "").replace("'", '"')
				cmd = self.new_js + "var a = '" + content + "';" + "return t(a);"
				#print cmd
				l = open("log.txt", "wb")
				l.write(cmd)
				l.close()
				rst = self.driver.execute_script(cmd)
				#print rst.encode('utf-8')#("ascii", "ignore")
				idx = path.find('resource/assets')
				filename = path[idx:]
				filename = filename.replace('.exml', '.js').replace('/', '_')
				filename = self.output_path + filename
				o = open(filename, "wb")
				o.write(rst.encode('utf-8'))
				o.close()
				
		def test(self):
				#sleep(10)
				rst = self.driver.execute_script(self.jj)
				#for k, v in rst.items():
				#		print k
				#o = open("log.txt", "wb")
				#o.write(str(rst))
				print rst

if __name__ == "__main__":
		e = EXML2JS()
		e.proc()
		print "success ", e.count