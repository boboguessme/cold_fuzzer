# -*- coding: utf-8

import random

# 随机数据模块

class Rand(object):
	def __init__(self, seed=None):
		"""
			@seed random seed
		"""
		if seed is None:
			random.seed()
		else:
			random.seed(seed)

	def rint(self, mod):
		"""
			@mod 
		"""
		return random.randint(0, mod)
	
	def rbool(self):
		""""""
		return True if self.rint(2) == 1 else False
		
if __name__ == '__main__':
	rand = Rand()
	print 'rint(10)\n%d\n\n' % rand.rint(10)
	print 'rbool()\n%s\n\n' % rand.rbool()
	