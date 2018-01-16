#-*- coding:utf-8 -*-
import wx

class map_editor(wx.Panel):
		def __init__(self, parent):
				wx.Frame.__init__(self, parent, size = (500, 500))
				self.control = wx.TextCtrl(self, value='map', style=wx.TE_MULTILINE)
				self.Show(True)
				
def init(parent):
		frame = map_editor(parent)
		return frame
				
if __name__ == "__main__":
		app = wx.App(False)
		frame = map_editor(None, "map Editor")
		app.MainLoop()