#-*- coding:utf-8 -*-

class DefMethod:
	func_id = -1
	func_name = ''
	args = []

class DefProperty:
	name = ''
	type_name = ''

class EntityDef:
	defs = {}
	default = None

	def __init__(self):
		self.props = {}
		self.base_methods = {}
		self.cell_methods = {}
		self.client_methods = {}
		pass

	def parse(self, xml):
		for node in xml:
			if node.tag == "Properties":
				self.parse_props(node)
			elif node.tag == "ClientMethods":
				self.parse_method(1, node)
			elif node.tag == "BaseMethods":
				self.parse_method(2, node)
			elif node.tag == "CellMethods":
				self.parse_method(3, node)

	def parse_props(self, xml):
		i = 0
		for node in xml:
			name = node.tag
			t = ""
			for arg in node:
				if arg.tag == "Type":
					t = arg.text.strip()

			p = DefProperty()
			p.name = name
			p.type_name = t
			self.props[i] = p
			i = i + 1
		pass

	def parse_method(self, t, xml):
		methods = self.base_methods
		if t == 1:
			methods = self.client_methods
		elif t == 2:
			methods = self.base_methods
		elif t == 3:
			methods = self.cell_methods
		i = 0
		for method in xml:
			name = method.tag
			args = []
			for arg in method:
				if arg.tag == 'Arg':
					args.append(arg.text.strip())
			m = DefMethod()
			m.func_id = i
			m.func_name = name
			m.args = args
			methods[i] = m
			i = i + 1
