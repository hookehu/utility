#-*- coding:utf-8 -*-
import wx

class png_editor(wx.Frame):
		def __init__(self, parent, title):
				wx.Frame.__init__(self, parent, title = title, size = (500, 500))
				self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
				self.Show(True)
				
if __name__ == "__main__":
		app = wx.App(False)
		frame = png_editor(None, "PNG Editor")
		app.MainLoop()