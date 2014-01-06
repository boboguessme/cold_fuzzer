# -*- coding: utf-8 -*-

import utils

#  JS变量类型转换
# TODO 考虑是否把declare、assign、invoke_function包装成一个statement类

class TYPE(object):
	NULL = 0
	NUMBER = 1
	STRING = 2
	VARIABLE = 3
	FUNCTION = 4	# TODO 还没有支持赋值语句定义匿名函数
	
	def __init__(self):
		""""""
		pass
		
	@staticmethod
	def convert(value, type):
		"""
			@value
			@type
		"""
		# 没有列表类型，补充的话应该可以直接str()转换
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
			
#  产生JS操作代码
			
class JsGen(object):
	def __init__(self, ids):
		"""
			@ids html elements
		"""
		self.ids = ids
		self.rand = utils.Rand()
		
	@staticmethod
	def declare(name, value=None, type=None):
		"""
			@name
			@value
			@type one of TYPE
		"""
		if value is None:
			return 'var %s;' % name
		else:
			# assign has added ;
			return 'var %s' % JsGen.assign(name, value, type)
		
	@staticmethod
	def assign(lvalue, rvalue, type):
		"""		
			@lvalue
			@rvalue
			@type ont of TYPE
		"""
		return '%s = %s;' % (lvalue, TYPE.convert(rvalue, type))
		
	
	@staticmethod
	def invoke_function(invoker, function, args={}):
		"""
			@invoker
			@function
			@args {type : value, ...}  
		"""
		args_helper = []
		for value, type in args.items():
			args_helper.append(TYPE.convert(value, type))
		args_str = ', '.join(args_helper)
		
		return '%s.%s(%s);' % (invoker, function, args_str)
		
	@staticmethod
	def create_function(name, arg_names=[], statements=[]):
		"""
			@name
			@arg_names
			@statements
		"""
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
		