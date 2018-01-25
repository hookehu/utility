#-*- coding:utf-8 -*-
import wx

class PNGEditorEvent(wx.PyCommandEvent):  #1 定义事件
		def __init__(self, evtType, id):
				wx.PyCommandEvent.__init__(self, evtType, id)
				self.eventArgs = ""
				
		def GetEventArgs(self):
				return self.eventArgs
				
		def SetEventArgs(self, args):
				self.eventArgs = args
		
myEVT_MY_TEST = wx.NewEventType() #2 创建一个事件类型
EVT_ADD_FILES = wx.PyEventBinder(myEVT_MY_TEST, wx.ID_ANY)
