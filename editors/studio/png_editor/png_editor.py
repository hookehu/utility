#-*- coding:utf-8 -*-
import wx
import os
from core import components

class png_editor(wx.Panel):
		def __init__(self, parent):
				wx.Panel.__init__(self, parent, size = parent.Size, style=wx.DOUBLE_BORDER)
				self.draging = False
				self.pen=wx.Pen(wx.Colour(0, 255, 0), 2) 
				self.brush = wx.Brush(wx.Colour(0, 255, 255, 100), style=wx.BRUSHSTYLE_TRANSPARENT)
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
				
				self.work_panel = wx.Panel(self, style=wx.DOUBLE_BORDER)
				self.right_sizer.Add(self.work_panel, flag=wx.EXPAND)
				self.bmps = [wx.Bitmap('frame_00001.png', wx.BITMAP_TYPE_PNG), wx.Bitmap('frame_00002.png', wx.BITMAP_TYPE_PNG), wx.Bitmap('frame_00003.png', wx.BITMAP_TYPE_PNG)]
				
				self.mask = wx.Panel(self.work_panel, size=self.bmps[0].Size)
				
				self.mask.Bind(wx.EVT_LEFT_DOWN, self.on_drag_begin)
				self.mask.Bind(wx.EVT_MOTION, self.on_draging)
				self.mask.Bind(wx.EVT_LEFT_UP, self.on_drag_end)
				self.mask.Bind(wx.EVT_PAINT, self.on_paint, self.mask)
				
				self.buffer=wx.Bitmap(self.mask.Size[0], self.mask.Size[1])
				
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
				
		def on_drag_begin(self, evt):
				#print "drag begin", evt.GetPosition()
				 
				self.pre_pos = evt.GetPosition()
				self.draging = True
				
		def on_draging(self, evt):
				if not self.draging:
						return
				self.cur_pos = evt.GetPosition()
				#print 'duck'
				
				dc = wx.BufferedDC(None, self.buffer, wx.BUFFER_VIRTUAL_AREA)  
				dc.SetBackground(self.brush)
				dc.Clear()
				for bp in self.bmps:
						dc.DrawBitmap(bp, 0, 0, True)
				dc.SetPen(self.pen)
				#dc.DrawRectangle(self.pre_pos[0], self.pre_pos[1], self.cur_pos[0] - self.pre_pos[0], self.cur_pos[1] - self.pre_pos[1])
				w = self.cur_pos[0] - self.pre_pos[0]
				h = self.cur_pos[1] - self.pre_pos[1]
				dc.DrawLine(self.pre_pos, self.pre_pos + (w, 0))
				dc.DrawLine(self.pre_pos + (w, 0), self.cur_pos)
				dc.DrawLine(self.cur_pos, self.pre_pos + (0, h))
				dc.DrawLine(self.pre_pos, self.pre_pos + (0, h))
				self.mask.Refresh()
				pass
				
		def on_drag_end(self, evt):
				self.draging = False
				self.pre_pos = None
				
				pass
				
		def on_paint(self, evt):
				#print 'draw', self.work_panel.GetChildren()
				wx.BufferedPaintDC(self.mask, self.buffer)
				pass
				
def init(parent):
		frame = png_editor(parent)
		return frame
				
if __name__ == "__main__":
		app = wx.App(False)
		frame = png_editor(None, "PNG Editor")
		app.MainLoop()