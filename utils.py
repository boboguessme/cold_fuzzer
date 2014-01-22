# -*- coding: utf-8

import random

## 随机实用类
class Rand(object):

	_CHARS = [
		'A', 'B', 'C', 'D', 'E', 'F',
		'G', 'H', 'I', 'J', 'K', 'L',
		'M', 'N', 'O', 'P', 'Q', 'R',
		'S', 'T', 'U', 'V', 'W', 'X', 
		'Y', 'Z', 'a', 'b', 'c', 'd', 
		'e', 'f', 'g', 'h', 'i', 'j', 
		'k', 'l', 'm', 'n', 'o', 'p', 
		'q', 'r', 's', 't', 'u', 'v', 
		'w', 'x', 'y', 'z', '_',
	]
	
	## 构造函数
	#  @param seed 随机种子
	def __init__(self, seed=None):
		if seed is None:
			random.seed()
		else:
			random.seed(seed)

	## 生成随机整数
	#  @param mod 生成整数最大值
	#  @return 随机整数在0 -- (mod-1)
	def rint(self, mod):
		return random.randint(0, mod-1)
	
	## 生成随机布尔值
	#  @return 随机布尔值
	#  @attention 返回值是字符串形式
	def rbool(self):
		return 'true' if self.rint(2) == 1 else 'false'
		
	## 生成指定长度随机字符串
	#  @param str_len 字符串长度
	#  @return 随机字符串
	def rstr(self, str_len):
		str_helper = []
		while len(str_helper) < str_len:
			str_helper.append(random.choice(self._CHARS))
		return ''.join(str_helper)
		
	## 混杂两个列表
	#  @param seq1
	#  @param seq2
	#  @return 混杂合并的列表
	def rmix(self, seq1, seq2):
		return random.sample(seq1+seq2, len(seq1)+len(seq2))
		
if __name__ == '__main__':
	rand = Rand()
	print 'rint(10)\n%d\n\n' % rand.rint(10)
	print 'rbool()\n%s\n\n' % rand.rbool()
	print 'rstr(10)\n%s\n\n' % rand.rstr(10)
	