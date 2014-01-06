# -*- coding: utf-8 -*-

from tag import Tag

#  产生元素相关的页面代码

class Element(object):
	def __init__(self, element_tag):
		"""
			@element_tag
		"""
		self.tag = Tag(element_tag)
		self.attributes = {}
		self.text = ''
		self.sub_elements = []
		
	def set_attribute(self, name, value):
		"""
			@name attribute
			@value
		"""
		self.attributes[name] = value
	
	def set_text(self, text):
		"""
			@text text node
		"""
		self.text = text
		
	def append_child(self, element):
		"""
			@element html element
		"""
		self.sub_elements.append(element)
		
	def open(self):
		""""""
		return self.tag.open(self.attributes, self.text)
		
	def close(self):
		""""""
		return self.tag.close()
		
	def convert_to_code(self):
		"""
			@return elements tree html code
		"""
		code_helper = []
		reverse_sub_elements = []
		code_helper.append(self.open())
		for element in self.sub_elements:
			code_helper.append(element.convert_to_code())
		code_helper.append(self.close())
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