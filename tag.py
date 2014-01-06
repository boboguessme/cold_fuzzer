# -*- coding: utf-8 -*-

#  产生元素的打开、闭合和text节点
#   支持attribute text
#   FIXME 支持很小一部分没有闭合的tag

class Tag(object):
	no_end_tags = ['br', 'link']  	# TODO 补充元素列表
	def __init__(self, tag):
		"""
			@tag element tag
		"""
		self.tag = tag.lower()
		
	def open(self, attributes={}, text=''):
		"""
			@attributes {name : value, ...}
			@text string
		"""
		content = '<%s' % self.tag
		for name, value in attributes.items():
			content = ' '.join((content, '%s="%s"' % (name, value)))
		if self.tag in self.no_end_tags:
			content = ''.join((content, '>'))
		else:
			content = ''.join((content, '>', text))
		return content
		
	def close(self):
		""""""
		if self.tag in self.no_end_tags:
			return ''
		else:
			return '</%s>' % self.tag
		
if __name__ == '__main__':
	tag = Tag('html')
	print 'open()\n%s\n\n' % tag.open()
	print 'open(text="L")\n%s\n\n' % tag.open(text="L")
	print 'open({id="test", width="4"})\n%s\n\n' % tag.open({'id':'test', 'width':'4'})
	print 'open({id="test", width="4"}, "L")\n%s\n\n' % tag.open({'id':'test', 'width':'4'}, "L")
	print 'close()\n%s\n\n' % tag.close()
	tag = Tag('br')
	print 'open()\n%s\n\n' % tag.open()
	print 'close()\n%s\n\n' % tag.close()
	tag = Tag('link')
	print 'open(text="L")\n%s\n\n' % tag.open(text="L")
	print 'open({id="test", width="4"})\n%s\n\n' % tag.open({'id':'test','width':'4'})
	print 'close()\n%s\n\n' % tag.close()	