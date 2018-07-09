import sys
import os as myos
import test_import as my_module

def myfunc(args = None, second_l = "hhh"):
	var = 2
	print var, args
	lvar = 3
	def _lambda():
		print lvar, second_l
	return _lambda

class MyClass(object):
	def __init__(self):
		myid = 123
		self.id = myid

	def myfunc(self):
		print self.id + 100

myfunc(args = "this is test args")()

obj = MyClass()
print obj.id

obj.myfunc()
print getattr(obj, "myfunc")

print my_module.sum("abc ", "egf")

print my_module.do_something()
