# -*- coding: utf-8 -*-

import utils

## js变量类型转换
#  @todo 考虑是否把declare、assign、invoke_function包装成一个statement类
#  @todo 没有支持赋值语句定义匿名函数
class TYPE(object):

	## JavaScript NULL显示形式
	NULL = 0
	## JavaScript 数字显示形式
	NUMBER = 1
	## JavaScript 字符串显示形式
	STRING = 2
	## JavaScript 变量显示形式
	VARIABLE = 3
	## JavaScript 函数显示形式
	FUNCTION = 4
	
	## 构造函数
	def __init__(self):
		pass
		
	## 将类型转换成显示形式
	#  @param value 显示值
	#  @param type 显示类型
	#  @return 对应值的显示形式
	#  @return 如果不支持的显示类型，返回'null'
	#  @remark 没有列表类型，补充的话应该可以直接str()转换
	@staticmethod
	def convert(value, type):
		if type == TYPE.NULL:
			return 'null'
		elif type == TYPE.NUMBER:
			return str(value)
		elif type == TYPE.STRING:
			return '"%s"' % value
		elif type == TYPE.VARIABLE:
			return value
		else:
			return 'null'
			
## js代码生成		
#  @remark 分支和循环太高级，就不支持了 - -#	
#  @attention 为了简单起见，每一个元素的引用变量和id一致
class JsGen(object):
	
	## @var ELEMENTS
	#  @todo 补齐列表
	#  元素列表
	ELEMENTS = ['CANVAS',]
	
	## @var EVENTS
	#  @todo 补齐列表
	#  事件列表
	EVENTS = ['select',]
	
	## @var COMMANDS
	# @todo 补齐列表
	#  命令列表
	COMMANDS = ['delete',]
	
	## @var INTERESTING_VALUES
	#  特殊值列表
	INTERESTING_VALUES = [
		TYPE.convert(0, TYPE.NUMBER),
	]
	
	## @var MAX_OPERATIONS
	#  fuzz最大操作上限
	MAX_OPERATIONS = 50
	
	## @var MAX_ELEMENTS
	#  添加元素数量随机mod
	MAX_ELEMENTS = 20
	
	## @var MAX_PROPERTY
	#  添加属性数量随机mod
	MAX_PROPERTY = 9
	
	## @var MAX_LISTENERS
	#  添加事件数量随机mod
	MAX_LISTENERS = 5
	
	## @var ids
	#  页面元素id列表	
	## @var rand
	#  随机数据对象
	
	## 构造函数
	#  @param ids 页面元素id列表
	def __init__(self, ids):
		self.ids = ids
		self.rand = utils.Rand()
		
	## 初始化分配html元素变量引用
	#  @return 声明已存在元素的js代码序列
	#  @remark 这一会因为invoke_function自动添加';'导致每条语句多出一个';'
	def init_vars(self):
		js_content = []
		for id in self.ids:
			js_content.append(self.declare(
						id,
						self.invoke_function(
							'document', 'getElementById', {id:TYPE.STRING}),
						TYPE.VARIABLE))
		return js_content
		
	## fuzz策略生成
	#  @return fuzz操作js代码
	#  @remark 起点函数是cold_start
	def fuzz(self):
		js_content = []		
		js_content.extend(self.init_vars())
		operation_counts = self.rand.rint(self.MAX_OPERATIONS)
		for current_operation_count in xrange(operation_counts):
			js_content.append(self.random_operate())
		cold_start = self.create_function('cold_start', [], js_content)
		return cold_start
	
	## 随机操作
	#  @return 随机操作的js代码
	def random_operate(self):
		type_mod = 4
		type = self.rand.rint(type_mod)
		# 事件操作
		if type == 0:
			return self.random_event_operate()
		# 样式操作
		elif type == 1:
			return self.random_style_operate()
		# 元素操作
		elif type == 2:
			return self.random_element_operate()
		# 全局操作
		else:
			return self.random_global_operate()
			
	## 随机事件操作
	#  @return 相应js代码
	#  @attention 包含相关函数定义
	def random_event_operate(self):
		####### TODO  干活
		return self.invoke_function('window', 'alert', {'event':TYPE.STRING})
		
	## 随机样式操作
	#  @return 相应js代码
	def random_style_operate(self):
		####### TODO  干活
		return self.invoke_function('window', 'alert', {'style':TYPE.STRING})
		
	## 随机元素操作
	#  @return 相应js代码
	def random_element_operate(self):
		type_mod = 4
		type = self.rand.rint(type_mod)
		# 增加元素，并随机添加到tree中
		if type == 0:
			js_content = []
			js_content.append(self.setup_element(self.random_item(self.ELEMENTS)))
			# 添加的元素id应该是ids的最后一个元素
			element_id = self.ids[-1]
			js_content.append(self.invoke_function(
					self.random_item(self.ids),
					'appendChild',
					{element_id:TYPE.VARIABLE}))
			return ''.join(js_content)		
		# 删除元素
		elif type == 1:
			# TODO removeNode貌似只有IE支持，以后考虑考虑
			# 现在只用了removeChild
			current_element = self.random_item(self.ids)
			return self.invoke_function(
				'.'.join((current_element, 'parentNode')),
				'removeChild', {current_element:TYPE.VARIABLE})
		# 清空元素内容
		elif type == 2:
			# TODO 随机是innerHTML等啥乱七八糟置为null
			return self.assign(
				'.'.join((self.random_item(self.ids), 'innerHTML')),
				'null', TYPE.NULL)		
		# 引用元素
		# 随机选取元素添加到另一随意元素
		else:
			child_element = self.random_item(self.ids)
			parent_element = self.random_item(self.ids)
			return self.invoke_function(
				parent_element, 'appendChild', {child_element:TYPE.VARIABLE})
		
	## 随机全局操作
	#  @return 相应js代码
	def random_global_operate(self):
		####### TODO  干活
		return self.invoke_function('window', 'alert', {'global':TYPE.STRING})
		
	## 创建元素，赋值变量并且设置元素id为对应变量名
	#  @param element_tag 元素tag名称
	#  @param id_len id长度，默认10
	#  @return 相应js代码
	def setup_element(self, element_tag, id_len=10):
		element_id = self.rand.rstr(id_len)
		self.ids.append(element_id)
		return 'var %s = %s;%s' % (element_id, 
					self.create_element(element_tag),
					self.set_element_id(element_id))
		
	## 随机创建元素
	#  @return 相应js代码
	def random_create_element(self):
		return self.create_element(self.random_item(self.ELEMENTS))
		
	## 创建元素
	#  @param element_tag 元素tag名称
	#  @return 相应js代码
	def create_element(self, element_tag):
		return 'document.createElement("%s")' % element_tag

	## 随机挑选元素添加随机子元素
	#  @return 相应js代码
	def random_append_element(self):
		return self.append_element(self.random_item(self.ids),
			self.random_item(self.ids))
	
	## 添加子元素
	#  @param parent 父元素变量名
	#  @param child 子元素变量名
	#  @return 相应js代码
	def append_element(self, parent, child):
		return '%s.appendChild(%s);' % (parent, child)
	
	## 设置元素id
	#  @param element_id 元素变量名也是对应id
	#  @return 相应js代码
	def set_element_id(self, element_id):
		lvalue = ''.join((element_id, '.id'))
		return self.assign(lvalue, element_id, TYPE.STRING)
		
	## 随机获取给定列表元素
	#  @param items
	#  @return 相应js代码
	def random_item(self, items):
		return items[self.rand.rint(len(items))]
		
	## 生成变量声明语句
	#  @param name 变量名
	#  @param value 变量值
	#  @param type js.TYPE 支持类型
	#  @return 变量声明语句
	#  @remark 代码已经添加';'
	@staticmethod
	def declare(name, value=None, type=None):
		if value is None:
			return 'var %s;' % name
		else:
			# assign函数已经添加了';'，所以这里不需要追加
			return 'var %s' % JsGen.assign(name, value, type)
		
	## 生成赋值语句
	#  @param lvalue 赋值左值
	#  @param rvalue 赋值右值
	#  @param type js.TYPE 支持类型
	#  @return 赋值语句
	#  @remark 代码已经添加';'
	@staticmethod
	def assign(lvalue, rvalue, type):
		return '%s = %s;' % (lvalue, TYPE.convert(rvalue, type))
		
	## 生成函数调用语句
	#  @param invoker 函数所属对象 
	#  @param function 函数名
	#  @param args 函数参数 {参数值:js.TYPE 支持类型}
	#  @return 函数调用语句
	#  @remark 代码已经添加';'
	#  @attention invoker不可为空，比如alert应以window.alert形式调用
	@staticmethod
	def invoke_function(invoker, function, args={}):
		args_helper = []
		for value, type in args.items():
			args_helper.append(TYPE.convert(value, type))
		args_str = ', '.join(args_helper)
		
		return '%s.%s(%s);' % (invoker, function, args_str)
		
	## 生成函数定义
	#  @param name 函数名
	#  @param arg_names 函数参数表
	#  @param statements 函数的语句序列
	#  @return 函数定义代码
	@staticmethod
	def create_function(name, arg_names=[], statements=[]):
		return 'function %s(%s){%s}' % \
			(name, ', '.join(arg_names), ''.join(statements))
		
if __name__ == '__main__':
	print 'declare has tested assign'
	print 'declare("test")\n%s\n\n' % JsGen.declare('test')
	print 'declare("test", 12, TYPE.NUMBER)\n%s\n\n' % JsGen.declare('test', 12, TYPE.NUMBER)
	print 'declare("test", "null", TYPE.NULL)\n%s\n\n' % JsGen.declare('test', 'null', TYPE.NULL)
	print 'declare("test", "test_str", TYPE.STRING)\n%s\n\n' % JsGen.declare('test', 'test_str', TYPE.STRING)
	print 'declare("test", "test", TYPE.VARIABLE)\n%s\n\n' % JsGen.declare('test', 'test', TYPE.VARIABLE)
	print 'invoke_function("document", "createRange")\n%s\n\n' % JsGen.invoke_function('document', 'createRange')
	print 'invoke_function("window", "alert", {"hello world!" : TYPE.STRING})\n%s\n\n' % JsGen.invoke_function('window', 'alert', {'hello world!' : TYPE.STRING})
	print 'invoke_function("div_s", "setAttribute", {"test_attr":TYPE.STRING, "test_value":TYPE.STRING})\n%s\n\n' % JsGen.invoke_function('div_s', 'setAttribute', {'test_attr':TYPE.STRING, 'test_value':TYPE.STRING})
	print 'create_function("test_func")\n%s\n\n' % JsGen.create_function('test_func')
	print 'create_function("test_func", ["a","b","c"])\n%s\n\n' % JsGen.create_function('test_func', ['a','b','c'])
	print 'create_function("test_func", statements=[declare("test", "test_str", TYPE.STRING), invoke_function("document", "createRange")])\n%s\n\n' % JsGen.create_function('test_func', statements=[JsGen.declare('test', 'test_str', TYPE.STRING), JsGen.invoke_function('document', 'createRange')])
	print 'create_function("test_func", ["a","b","c"], [declare("test", "test_str", TYPE.STRING), invoke_function("document", "createRange")])\n%s\n\n' % JsGen.create_function('test_func', ['a', 'b', 'c'], [JsGen.declare('test', 'test_str', TYPE.STRING), JsGen.invoke_function('document', 'createRange')])
	
	jg = JsGen(['a', 'b'])
	print 'random_append_element()\n%s\n\n' % jg.random_append_element()
	print 'setup_element("div")\n%s\n\n' % jg.setup_element('div')
	print 'fuzz()\n%s\n\n' % jg.fuzz()
		