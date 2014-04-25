# -*- coding: utf-8 -*-

from element import Element
from js import JsGen

## 代表整个生成页面代码
class PageHolder(object):

	## @var MAX_INIT_ELEMENTS
	#  最大初始化元素个数
	MAX_INIT_ELEMENTS = 8
	
	## @var MAX_STYLE_COUNTS
	#  最大style样式个数
	MAX_STYLE_COUNTS = 3

	## 构造函数
	#  @todo 还在纠结是不是要添加<!doctype html>  fuzz SVG可能就不能增加
	def __init__(self):
		# html5头
		self._htmlpage = '<!DOCTYPE html>'
		self._ids = []
		self._elements = []
		self._jsgen = JsGen([])
		
	## 构造元素树
	#  @param id_len id长度，默认10
	#  @return element.Element 对象
	def build_element_tree(self, id_len=10):
		root = Element('html')
		
		if self._jsgen.rand.rint(2):
			style = Element('style')
			style.set_text('*{%s}' % self._jsgen.generate_style_attribute(
						self._jsgen.rand.rint(self.MAX_STYLE_COUNTS)))
			root.append_child(style)
		
		body = Element('body')
		body.set_attribute('id', 'body')
		body.set_attribute('onload', 'cold_start()')
		root.append_child(body)
		self._ids.append('body')
		self._elements.append(body)
		

		init_element_counts = self._jsgen.rand.rint(self.MAX_INIT_ELEMENTS)
		for i in xrange(init_element_counts):
			ele = Element(self._jsgen.random_item(self._jsgen.ELEMENTS))
			ele_id = self._jsgen.rand.rstr(id_len)
			ele.set_attribute('id', ele_id)
			self._jsgen.random_item(self._elements).append_child(ele)
			self._ids.append(ele_id)
			self._elements.append(ele)
			
			if self._jsgen.rand.rint(4) == 0:
				# style初始化处理
				ele.set_attribute('style', self._jsgen.generate_style_attribute(
							self._jsgen.rand.rint(self.MAX_STYLE_COUNTS)))
			
			if self._jsgen.rand.rint(4) == 0:
				# text节点处理
				ele.set_text('AAAAAAAA')
		return root
	
	## 生成页面
	#  @return 页面代码
	def dump_html(self):
		tree = self.build_element_tree()
		script = Element('script')
		script.set_text(JsGen(self._ids).fuzz())
		tree.append_child(script)
		return ''.join((self._htmlpage, tree.convert_to_code()))
		
if __name__ == '__main__':
	page = PageHolder()
	
	import os
	with open(os.path.join('test', 'test_pageholder.html'), 'wb') as f:
		f.write(page.dump_html())
		