# -*- coding: utf-8

import random

## 随机实用类
class Rand(object):
	
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
	#  @attention 返回值是python布尔形式
	def rbool(self):
		return True if self.rint(2) == 1 else False
		
if __name__ == '__main__':
	rand = Rand()
	print 'rint(10)\n%d\n\n' % rand.rint(10)
	print 'rbool()\n%s\n\n' % rand.rbool()
	