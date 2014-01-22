# -*- coding: utf-8 -*-

from element import Element
from js import JsGen

## 代表整个生成页面代码
class PageHolder(object):

	## 构造函数
	#  @todo 还在纠结是不是要添加<!doctype html>
	def __init__(self):
		# html5头
		self._page = '<!doctype html>'
		self._ids = []
		self._tree = None
		self._js = None
		
	## 构造元素树
	#  @return element.Element 对象
	#  @todo 未实现
	def build_element_tree(self):
		tree = Element('html')
		
		body = Element('body')
		body.set_attribute('id', 'body')
		self._ids.append('body')
		tree.append_child(body)
		body.set_attribute('onload', 'cold_start()')
		
		div = Element('div')
		div.set_attribute('id', 'my_div')
		self._ids.append('my_div')
		div.set_attribute('align', 'center')
		body.append_child(div)
		
		h1 = Element('h1')
		h1.set_attribute('id', 'h1')
		self._ids.append('h1')
		h1.set_text('hello')
		div.append_child(h1)
		
		h2 = Element('h2')
		h2.set_attribute('id', 'h2')
		self._ids.append('h2')
		h2.set_text('world')
		div.append_child(h2)
		
		return tree
	
	## 生成页面
	#  @return 页面代码
	def dump(self):
		self._tree = self.build_element_tree()
		self._js = JsGen(self._ids).fuzz()
		script = Element('script')
		script.set_text(self._js)
		self._tree.append_child(script)
		return self._tree.convert_to_code()
		
if __name__ == '__main__':
	page = PageHolder()
	
	import os
	with open(os.path.join('test', 'test_pageholder.html'), 'wb') as f:
		f.write(page.dump())
		