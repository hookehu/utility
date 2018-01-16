#-*- coding:utf-8 -*-
import wx

class act_editor(wx.Panel):
		def __init__(self, parent):
				wx.Frame.__init__(self, parent, size = (500, 500))
				self.control = wx.TextCtrl(self, value='act', style=wx.TE_MULTILINE)
				self.Show(True)
				
def init(parent):
		frame = act_editor(parent)
		return frame
				
if __name__ == "__main__":
		app = wx.App(False)
		frame = act_editor(None, "act Editor")
		app.MainLoop()