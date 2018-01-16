#-*- coding:utf-8 -*-
import wx
from core import *

class png_editor(wx.Panel):
		def __init__(self, parent):
				wx.Panel.__init__(self, parent, size = (500, 500))
				self.control = wx.TextCtrl(self, value='png', style=wx.TE_MULTILINE)
				self.Show(True)
				
def init(parent):
		frame = png_editor(parent)
		return frame
				
if __name__ == "__main__":
		app = wx.App(False)
		frame = png_editor(None, "PNG Editor")
		app.MainLoop()