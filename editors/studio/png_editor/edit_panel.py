#-*- coding:utf-8 -*-
import wx

class edit_panel(wx.Panel):
		def __init__(self, parent, id, style):
				wx.Panel.__init__(self, parent, style = style)
				self.init_ui()
				
		def init_ui(self):
				self.xd = wx.StaticText(self, -1, "x:")
				self.x = wx.TextCtrl(self, size = (80, 30))
				self.yd = wx.StaticText(self, -1, "y:")
				self.y = wx.TextCtrl(self, size = (80, 30))
				self.wd = wx.StaticText(self, -1, "w:")
				self.w = wx.TextCtrl(self, size = (80, 30))
				self.hd = wx.StaticText(self, -1, "h:")
				self.h = wx.TextCtrl(self, size = (80, 30))
				self.sd = wx.StaticText(self, -1, "scale:")
				self.scale = wx.TextCtrl(self, size = (80, 30))
				
				self.modify_btn = wx.Button(self, label = u"修改", size = (80, 30))
				self.save_btn = wx.Button(self, label = u"保存", size = (80, 30))
				self.Bind(wx.EVT_BUTTON, self.on_modify_click, self.modify_btn)
				self.Bind(wx.EVT_BUTTON, self.on_save_click, self.save_btn)
				
				self.init_sizer()
				
		def init_sizer(self):
				self.edit_sizer = wx.BoxSizer(wx.HORIZONTAL)
				self.edit_sizer.Add(self.xd, border = 10)
				self.edit_sizer.Add(self.x, border=10)
				self.edit_sizer.Add(self.yd, border = 10)
				self.edit_sizer.Add(self.y, border=10)
				self.edit_sizer.Add(self.wd, border = 10)
				self.edit_sizer.Add(self.w, border=10)
				self.edit_sizer.Add(self.hd, border = 10)
				self.edit_sizer.Add(self.h, border=10)
				self.edit_sizer.Add(self.sd, border = 10)
				self.edit_sizer.Add(self.scale, border = 10)
				self.edit_sizer.Add(self.modify_btn, border=10)
				self.edit_sizer.Add(self.save_btn, border = 10)
				self.SetSizer(self.edit_sizer)
				
		def on_modify_click(self, evt):
				print "click"
				
		def on_save_click(self, evt):
				print 'save'
				
		def set_data(self, x, y, w, h):
				self.x.SetLabel(x + "")
				self.y.SetLabel(y + "")
				self.w.SetLabel(w + "")
				self.h.SetLabel(h + "")