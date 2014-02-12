# -*- coding: utf-8 -*-

from element import Element
from js import JsGen

## 代表整个生成页面代码
#  @todo 增加style标签
class PageHolder(object):

	## @var MAX_INIT_ELEMENTS
	#  最大初始化元素个数
	MAX_INIT_ELEMENTS = 8

	## 构造函数
	#  @todo 还在纠结是不是要添加<!doctype html>  fuzz SVG可能就不能增加
	def __init__(self):
		# html5头
		self._page = '<!doctype html>'
		self._ids = []
		self._elements = []
		
	## 构造元素树
	#  @param id_len id长度，默认10
	#  @return element.Element 对象
	#  @todo 随机初始化元素style或者其他属性
	def build_element_tree(self, id_len=10):
		root = Element('html')
		body = Element('body')
		body.set_attribute('id', 'body')
		body.set_attribute('onload', 'cold_start()')
		root.append_child(body)
		self._ids.append('body')
		self._elements.append(body)
		
		jsgen = JsGen([])
		init_element_counts = jsgen.rand.rint(self.MAX_INIT_ELEMENTS)
		for i in xrange(init_element_counts):
			ele = Element(jsgen.random_item(jsgen.ELEMENTS))
			ele_id = jsgen.rand.rstr(id_len)
			ele.set_attribute('id', ele_id)
			jsgen.random_item(self._elements).append_child(ele)
			self._ids.append(ele_id)
			self._elements.append(ele)
	
		return root
	
	## 生成页面
	#  @return 页面代码
	def dump(self):
		tree = self.build_element_tree()
		script = Element('script')
		script.set_text(JsGen(self._ids).fuzz())
		tree.append_child(script)
		return tree.convert_to_code()
		
if __name__ == '__main__':
	page = PageHolder()
	
	import os
	with open(os.path.join('test', 'test_pageholder.html'), 'wb') as f:
		f.write(page.dump())
		