# -*- coding: utf-8 -*-

## 代表整个生成页面代码
class PageHolder(object):

	## 构造函数
	def __init__(self):
		# html5头
		self._page = '<!doctyle html>'
		self._tree = []
	
	#def add_element(self, ele):
	#	pass