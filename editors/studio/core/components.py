#-*- coding:utf-8 -*-
class TreeCtrlData:
		def __init__(self):
				self.name = ''
				self.is_folder = False
				self.is_open = False
				self.children = []
				self.open_img = wx.TreeItemIcon_Expanded
				self.close_img = wx.TreeItemIcon_Normal
				
class MyTreeCtrl(wx.TreeCtrl):
		def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TR_DEFAULT_STYLE, validator=wx.DefaultValidator, name=""):
				wx.TreeCtrl.__init__(self, parent, id, pos, size, style, validator, name)
				self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.on_collapsed)
				self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.on_expanded)
				self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_right_click)
				self.Bind(wx.EVT_TREE_ITEM_MENU, self.on_menu)
				self.init_ui()
				
		def init_ui(self):
				self.il = wx.ImageList(16, 16, True)
				self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
				self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16)))
				self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
				self.SetImageList(self.il)
				
		def refresh_data(self, root):
				self.data_dict = {}
				self.data = root
				self.DeleteAllItems()
				self.root = self.AddRoot(root.name)
				self.data_dict[self.root.GetID()] = root
				self.SetItemImage(self.root, 0, which=root.close_img)
				self.SetItemImage(self.root, 1, which=root.open_img)
				for child in root.children:
						item = self.AppendItem(self.root, child.name, data = child)
						self.SetItemText(item, child.name)
						if not child.is_folder:
								continue
						self.SetItemImage(item, 0, which=child.close_img)
						self.SetItemImage(item, 1, which=child.open_img)
						if len(child.children) == 0:
								continue
						self.add_children(item, child)
				self.Expand(self.root)
				
		def add_children(self, parent, node_data):
				for child in node_data.children:
						item = self.AppendItem(parent, child.name, data = child)
						self.SetItemText(item, child.name)
						if not child.is_folder:
								continue
						self.SetItemImage(item, 0, which = node_data.close_img)
						self.SetItemImage(item, 1, which = node_data.open_img)
						if len(child.children) == 0:
								continue
						self.add_children(item, child)
				if node_data.is_open:
						self.Expand(parent) #有子节点才有Expand效果
				
		def on_collapsed(self, evt):
				d = evt.GetItem()
				data = self.GetItemData(d)
				if data is None:
						return
				data.is_open = False
				
		def on_expanded(self, evt):
				d = evt.GetItem()
				data = self.GetItemData(d)
				if data is None:
						return
				data.is_open = True
				
		def on_menu(self, evt):
				print 'on_menu'
				
		def on_right_click(self, evt):
				print "fuck"
				
class TreePanel(wx.Panel):
		def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=""):
				wx.Panel.__init__(self, parent, id, pos, size, style, name)
				self.tree = MyTreeCtrl(self, -1, size=size, style=wx.TR_MULTIPLE|wx.TR_HAS_BUTTONS|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HAS_VARIABLE_ROW_HEIGHT|wx.TR_ROW_LINES)
				#self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_open)
				self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.right_click)
				self.init_data()
				
		def init_data(self):
				root = TreeCtrlData()
				root.name = 'root'
				sub = TreeCtrlData()
				sub.name = 'sub1'
				root.children.append(sub)
				sub = TreeCtrlData()
				sub.name = 'sub2'
				sub.is_open = True
				sub.is_folder = True
				root.children.append(sub)
				sub1 = TreeCtrlData()
				sub1.name = 'sub21'
				sub.children.append(sub1)
				self.tree.refresh_data(root)
				
		def init_data(self, datas):
				pass
				
		def init_dir(self, path):
				pass
				
		def get_root(self, path):
				pass
				
		def on_open(self, evt):
				paths = self.tree.GetSelections()
				print paths
				
		def right_click(self, evt):
				paths = self.tree.GetSelections()
				print paths