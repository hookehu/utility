#-*- coding:utf-8 -*-
class TimeLine:
		def __init__(self, frame_time):
				self.frame_time = frame_time
				self.handler = wx.EvtHandler()
				self.timer = wx.Timer(self.handler)
				self.handler.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
				self.timer.Start(self.frame_time)
				self.mgrs = []
				self.pre_time = 0
				
		def on_timer(self, evt):
				print time.time()
				cur_time = time.time() * 1000
				interval = cur_time - self.pre_time
				if self.pre_time == 0:
						interval = 0
				self.pre_time = cur_time
				for mgr in self.mgrs:
						try:
								mgr.update(interval)
						except:
								continue
				
		def set_frame_time(self, frame_time):
				self.frame_time = frame_time
				self.timer.Stop()
				self.timer.Start(self.frame_time)
				
		def register(self, mgr):
				self.mgrs.append(mgr)
				
class TimeLineMgr:
		def __init__(self):
				pass
				
		def update(self, interval):
				pass