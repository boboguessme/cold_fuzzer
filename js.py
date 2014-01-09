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
class JsGen(object):
	
	## @var ELEMENTS
	#  @todo 补齐列表
	#  元素列表
	ELEMENTS = ["CANVAS",]
	
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
	INTERESTING_VALUES = [0,]
	
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
		