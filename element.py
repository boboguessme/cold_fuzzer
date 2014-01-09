# -*- coding: utf-8 -*-

from tag import Tag

## 产生元素树页面代码
#  @attention 元素包含的子元素按照添加顺序排列
class Element(object):

	## @var tag
	#  tag.Tag 对象
	## @var attributes
	#  元素属性
	## @var text
	#  text节点内容
	## @var sub_elements
	#  子元素
	
	## 构造函数
	#  @param element_tag tag.Tag 对象
	def __init__(self, element_tag):
		self.tag = Tag(element_tag)
		self.attributes = {}
		self.text = ''
		self.sub_elements = []
		
	## 设置元素属性
	#  @param name 属性名
	#  @param value 属性值
	def set_attribute(self, name, value):
		self.attributes[name] = value
	
	## 设置text节点内容
	#  @param text
	def set_text(self, text):
		self.text = text
		
	## 添加子元素
	#  @param element element.Element 对象
	def append_child(self, element):
		self.sub_elements.append(element)
		
	## 生成元素打开内容
	#  @return 元素打开代码
	def _open(self):
		return self.tag.open(self.attributes, self.text)
		
	## 生成元素闭合内容
	#  @return 元素闭合代码
	def _close(self):
		return self.tag.close()
		
	## 生成元素代码
	#  @return 对应元素树全部代码
	def convert_to_code(self):
		code_helper = []
		reverse_sub_elements = []
		code_helper.append(self._open())
		for element in self.sub_elements:
			code_helper.append(element.convert_to_code())
		code_helper.append(self._close())
		return ''.join(code_helper)
		
if __name__ == '__main__':
	html = Element('html')
	
	body = Element('body')
	html.append_child(body)
	
	div = Element('div')
	div.set_attribute('id', 'my_div')
	div.set_attribute('align', 'center')
	body.append_child(div)
	
	h1 = Element('h1')
	h1.set_text('hello')
	div.append_child(h1)
	
	h2 = Element('h2')
	h2.set_text('world')
	div.append_child(h2)
	
	import os
	with open(os.path.join('test', 'test_element.html'), 'wb') as f:
		f.write(html.convert_to_code())