#-*- coding:utf-8 -*-
import wx
import os
from core import components
from edit_panel import edit_panel

class png_editor(wx.Panel):
		def __init__(self, parent):
				wx.Panel.__init__(self, parent, size = parent.Size, style=wx.DOUBLE_BORDER)
				#self.SetAutoLayout(True)
				self.draging = False
				self.result_panel = None
				self.buffer = None
				self.pen=wx.Pen(wx.Colour(0, 255, 0), 2) 
				self.brush = wx.Brush(wx.Colour(255, 255, 255, 0), style=wx.BRUSHSTYLE_TRANSPARENT)
				self.bmps = []
				self.loaded_image = {}
				self.init_ui()
				self.init_data()
				self.Bind(wx.EVT_SIZE, self.on_size)
				self.Show(True)
				
		def on_size(self, evt):
				self.tree_panel.SetSize((250, self.Size[1]))
				
		def init_ui(self):
				self.tree_panel = components.TreePanel(self, size=(250, 250), style = wx.DOUBLE_BORDER)
				
				self.init_menu()
				
				self.edit = edit_panel(self, wx.ID_ANY, style=wx.DOUBLE_BORDER)
				
				self.work_panel = wx.Panel(self)
				
				self.result_panel = wx.Panel(self)
				
				self.work_panel.Bind(wx.EVT_LEFT_DOWN, self.on_drag_begin)
				self.work_panel.Bind(wx.EVT_MOTION, self.on_draging)
				self.work_panel.Bind(wx.EVT_LEFT_UP, self.on_drag_end)
				self.work_panel.Bind(wx.EVT_PAINT, self.on_paint)
				
				self.init_right_sizer()
				
		def init_right_sizer(self):
				self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
				self.left_sizer = wx.BoxSizer(wx.VERTICAL)
				self.right_sizer = wx.BoxSizer(wx.VERTICAL)
				
				self.main_sizer.Add(self.left_sizer)
				self.main_sizer.Add(self.right_sizer)
				self.left_sizer.Add(self.tree_panel)
				self.right_sizer.Add(self.edit, flag=wx.ALL|wx.ALIGN_TOP|wx.EXPAND)
				print self.work_panel.GetSize(), self.work_panel.GetMinSize()
				self.right_sizer.Add(self.work_panel, flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.FIXED_MINSIZE )
				self.right_sizer.Add(self.result_panel, flag = wx.ALL|wx.ALIGN_BOTTOM|wx.FIXED_MINSIZE )
				
				self.SetSizerAndFit(self.main_sizer)
				
		def init_menu(self):
				menu = wx.Menu()
				add = menu.Append(wx.ID_ANY, u"添加文件")
				self.Bind(wx.EVT_MENU, self.on_add_handler, add)
				self.tree_panel.set_menu(menu)
				
		def init_data(self):
				path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
				self.tree_panel.init_dir(path)
				
		def load_image(self, path):
				if os.path.isdir(path):
						files = os.listdir(path)
						for file in files:
								p = os.path.join(path, file)
								if os.path.isdir(p):
										self.load_image(p)
										continue
								self.load_one_image(p)
				else:
						self.load_one_image(path)
		
		def load_one_image(self, path):
				if self.loaded_image.has_key(path):
						return
				t = ""
				if path.find(".png") > 0:
						t = wx.BITMAP_TYPE_PNG
				elif path.find(".jpg") > 0:
						t = wx.BITMAP_TYPE_JPEG
				else:
						return
				self.loaded_image[path] = 1
				bmp = wx.Bitmap(path, t)
				self.bmps.append(bmp)
				
		def on_add_handler(self, evt):
				selections = self.tree_panel.get_selections()
				for select in selections:
						print select.path
						self.load_image(select.path)
				print self.bmps
				print 'aa', selections
				self.work_panel.SetSize(self.bmps[0].Size)
				self.work_panel.SetMinSize(self.bmps[0].Size)
				self.work_panel.SetMaxSize(self.bmps[0].Size)
				self.buffer = wx.Bitmap(self.bmps[0].Size[0], self.bmps[0].Size[1])
				dc = wx.BufferedDC(None, self.buffer, wx.BUFFER_VIRTUAL_AREA)  
				dc.SetBackground(self.brush)
				dc.Clear()
				for bp in self.bmps:
						dc.DrawBitmap(bp, 0, 0, True)
				
		def on_drag_begin(self, evt):
				if len(self.bmps) == 0:
						return
				if self.buffer == None:
						self.buffer = wx.Bitmap(self.work_panel.Size[0], self.work_panel.Size[1])
				self.pre_pos = evt.GetPosition()
				self.draging = True
				
		def on_draging(self, evt):
				if not self.draging:
						return
				self.cur_pos = evt.GetPosition()
				
				dc = wx.BufferedDC(None, self.buffer, wx.BUFFER_VIRTUAL_AREA)  
				dc.SetBackground(self.brush)
				dc.Clear()
				for bp in self.bmps:
						dc.DrawBitmap(bp, 0, 0, True)
				dc.SetPen(self.pen)
				
				w = self.cur_pos[0] - self.pre_pos[0]
				h = self.cur_pos[1] - self.pre_pos[1]
				dc.DrawLine(self.pre_pos, self.pre_pos + (w, 0))
				dc.DrawLine(self.pre_pos + (w, 0), self.cur_pos)
				dc.DrawLine(self.cur_pos, self.pre_pos + (0, h))
				dc.DrawLine(self.pre_pos, self.pre_pos + (0, h))
				self.work_panel.Refresh()
				
		def on_drag_end(self, evt):
				if not self.draging:
						return
				self.draging = False
				w = self.cur_pos[0] - self.pre_pos[0]
				h = self.cur_pos[1] - self.pre_pos[1]
				pw = w * len(self.bmps)
				ph = h
				self.result_panel.DestroyChildren()
				self.result_panel.SetSize(pw, ph)
				nb = wx.Bitmap(pw, ph)
				dc = wx.MemoryDC()
				dc.SelectObject(nb)
				dc.SetBackground(self.brush)
				dc.Clear()
				i = 0
				for bmp in self.bmps:
						dc.DrawBitmap(bmp.GetSubBitmap(wx.Rect(self.pre_pos, self.cur_pos)), i * w, 0, True)
						i = i + 1
				wx.StaticBitmap(self.result_panel, wx.ID_ANY, nb)
				print self.Size, self.result_panel.GetPosition(), pw, ph, self.work_panel.GetSize(), self.work_panel.GetMinSize(), self.work_panel.GetMaxSize(), self.work_panel.GetMinClientSize(), self.work_panel.GetVirtualSize(), self.work_panel.GetMinWidth(), self.work_panel.GetMinHeight(), self.work_panel.GetBestSize(), self.work_panel.GetRect(), self.work_panel.GetScreenRect()
				self.pre_pos = None
				p = (self.edit.Position[0], self.work_panel.Position[1] + self.work_panel.Size[1])
				self.result_panel.Move(p)
				
		def on_paint(self, evt):
				if not self.buffer:
						return
				wx.BufferedPaintDC(self.work_panel, self.buffer)
				
def init(parent):
		frame = png_editor(parent)
		return frame
				
if __name__ == "__main__":
		app = wx.App(False)
		frame = png_editor(None, "PNG Editor")
		app.MainLoop()