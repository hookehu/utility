#-*- coding:utf-8 -*-
import wx
import os
import setting

class MyFrame(wx.Frame):
		"""We simple derive a new class of Frame"""
		def __init__(self, parent, title):
				wx.Frame.__init__(self, parent, title=title,size=(600,600))
				self.cur_frame = None
				self.init_panels()
				self.init_menu()
				self.init_statusbar()
				self.Show(True)
				self.Bind(wx.EVT_SIZE, self.on_size)
				
		def on_size(self, evt):
				if self.cur_frame:
						self.cur_frame.SetSize(self.Size)
				
		def init_panels(self):
				#self.tree_panel = TreePanel(self)
				pass
				
		def gen_on_menu(self, container, k):
				def func(self):
						container.on_menu(k)
				return func
				
		def init_menu(self):
				filemenu = wx.Menu()
				for k, v in setting.APPS.items():
						menu = filemenu.Append(wx.ID_ANY, k, " ")
						print menu
						self.Bind(wx.EVT_MENU, self.gen_on_menu(self, k), menu)
						
				menu_exit = filemenu.Append(wx.ID_ANY, "Exit", "Termanate the program")
				filemenu.AppendSeparator()
				menu_about = filemenu.Append(wx.ID_ANY, "About", "Information about this program")#设置菜单的内容
				
				menuBar = wx.MenuBar()
				menuBar.Append(filemenu, u"编辑器")
				self.SetMenuBar(menuBar)#创建菜单条
				self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)#把出现的事件，同需要处理的函数连接起来
				
		def init_statusbar(self):
				self.CreateStatusBar()#创建窗口底部的状态栏
				
		def on_about(self,e):#about按钮的处理函数
				dlg = wx.MessageDialog(self,"A samll text editor", "About sample Editor",wx.OK)#创建一个对话框，有一个ok的按钮
				dlg.ShowModal()#显示对话框
				dlg.Destroy()#完成后，销毁它。

		def on_exit(self,e):
				self.Close(True)
				
		def on_menu(self, key):
				pkg = setting.APPS.get(key, None)
				print key, pkg
				if pkg:
						p = __import__(pkg)
						if self.cur_frame:
								self.cur_frame.Close()
								self.cur_frame = None
						self.cur_frame = p.init(self)
				
		def on_open(self,e):
				"""open a file"""
				self.dirname = ''
				dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)#调用一个函数打开对话框
				if dlg.ShowModal() == wx.ID_OK:
						self.filename = dlg.GetFilename()
						self.dirname = dlg.GetDirectory()
						self.address = os.path.join(self.dirname,self.filename)
						f = open(self.address,"r")
						file = (f.read()).decode(encoding='utf-8')#解码，使文件可以读取中文
						f.close()
						self.control.Clear()
						self.control.AppendText(file)#把打开的文件内容显示在多行文本框内
				dlg.Destroy()

		def on_save(self, e):
				date = (self.control.GetValue()).encode(encoding="utf-8")#编码，使中文可以正确存储
				f = open(self.address, 'w')
				f.write(date)
				f.close()#把文本框内的数据写入并关闭文件
				dlg = wx.MessageDialog(self, u"文件已经成功保存", u"消息提示", wx.OK)
				dlg.ShowModal()
				dlg.Destroy()

if __name__ == "__main__":
		app = wx.App(False)
		frame = MyFrame(None, '编辑器')
		app.MainLoop()