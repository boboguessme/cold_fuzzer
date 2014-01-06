# -*- coding: utf-8 -*-

class PageHolder(object):
	def __init__(self):
		""""""
		self.page = '<!doctyle html>'
		self.tree = []
	
	def add_element(self, ele):
		""""""
		pass
	

CURRENT_ELEMENTS = []

ELEMENTS = []
EVENTS = []
COMMANDS = []
	
def build_base_tree():
	""""""
	html = Tag('html')
	