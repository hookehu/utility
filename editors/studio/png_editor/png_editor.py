#-*- coding:utf-8 -*-
import wx
import os
from core import components

class png_editor(wx.Panel):
		def __init__(self, parent):
				wx.Panel.__init__(self, parent, size = parent.Size, style=wx.DOUBLE_BORDER)
				
				self.init_ui()
				self.init_data()
				self.Bind(wx.EVT_SIZE, self.on_size)
				self.Show(True)
				
		def on_size(self, evt):
				self.tree_panel.SetSize((250, self.Size[1]))
				
		def init_ui(self):
				self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
				self.left_sizer = wx.BoxSizer(wx.VERTICAL)
				self.right_sizer = wx.BoxSizer(wx.VERTICAL)
				self.edit_sizer = wx.BoxSizer(wx.HORIZONTAL)
				self.main_sizer.Add(self.left_sizer)
				self.main_sizer.Add(self.right_sizer)
				
				self.tree_panel = components.TreePanel(self, size=(250, 250), style = wx.DOUBLE_BORDER)
				self.left_sizer.Add(self.tree_panel, flag=wx.EXPAND)
				
				self.edit_panel = wx.Panel(self, style=wx.DOUBLE_BORDER)
				self.right_sizer.Add(self.edit_panel, flag=wx.EXPAND)
				
				self.x = wx.TextCtrl(self.edit_panel, size = (80, 30))
				self.edit_sizer.Add(self.x, border=10)
				self.y = wx.TextCtrl(self.edit_panel, size = (80, 30))
				self.edit_sizer.Add(self.y, border=10)
				self.w = wx.TextCtrl(self.edit_panel, size = (80, 30))
				self.edit_sizer.Add(self.w, border=10)
				self.h = wx.TextCtrl(self.edit_panel, size = (80, 30))
				self.edit_sizer.Add(self.h, border=10)
				self.line_num = wx.TextCtrl(self.edit_panel, size = (80, 30))
				self.edit_sizer.Add(self.line_num, border=10)
				self.modify_btn = wx.Button(self.edit_panel, label = u"修改", size = (80, 30))
				self.edit_sizer.Add(self.modify_btn, border=10)
				
				self.Bind(wx.EVT_BUTTON, self.on_modify_click, self.modify_btn)
				
				self.edit_panel.SetSizer(self.edit_sizer)
				
				self.SetSizerAndFit(self.main_sizer)
				
		def init_data(self):
				path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
				self.tree_panel.init_dir(path)
		
		def on_modify_click(self, evt):
				print "click"
				
def init(parent):
		frame = png_editor(parent)
		return frame
				
if __name__ == "__main__":
		app = wx.App(False)
		frame = png_editor(None, "PNG Editor")
		app.MainLoop()