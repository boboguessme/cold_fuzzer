# -*- coding: utf-8 -*-

## 产生元素打开、闭合和text节点的内容\n
#  支持attribute text
class Tag(object):

	## 不闭合的元素列表
	#  @todo 补充元素列表
	no_end_tags = ['br', 'link']
	
	## 构造函数
	#  @param tag 对应元素名称
	#  @remark tag不区分大小写
	def __init__(self, tag):
		self._tag = tag.lower()
		
	## 生成元素打开内容
	#  @param attributes {元素属性:属性值}
	#  @param text text节点内容
	#  @return 元素打开代码
	def open(self, attributes={}, text=''):
		content = '<%s' % self._tag
		for name, value in attributes.items():
			content = ' '.join((content, '%s="%s"' % (name, value)))
		if self._tag in self.no_end_tags:
			content = ''.join((content, '>'))
		else:
			content = ''.join((content, '>', text))
		return content
		
	## 生成元素闭合内容
	#  @return 元素闭合代码
	def close(self):
		if self._tag in self.no_end_tags:
			return ''
		else:
			return '</%s>' % self._tag
		
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