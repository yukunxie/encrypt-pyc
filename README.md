# encrypt-pyc
encrypt python pyc files.

# usage
python encrypt.py -h
usage: encrypt.py [-h] [--input INPUT] [--symbol SYMBOL]

encrypt pyc files. powered by realxie.

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    the target pyc or direcotry
  --symbol SYMBOL  the symbols file path


# testcase
## 1 uncompile test.pyc with uncompyle2
	realxie$ ncompyle2 test.pyc
	# 2018.07.09 14:27:09 DST
	#Embedded file name: test.py
	import sys
	import os as myos
	
	def myfunc(args = None, second_l = 'hhh'):
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
	
	
	myfunc(args='this is test args')()
	obj = MyClass()
	print obj.id
	obj.myfunc()
	print getattr(obj, 'myfunc')
	+++ okay decompyling test.pyc
	# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
	# 2018.07.09 14:27:09 DST


## 2 encrypt the pyc
	realxie$ python encrypt.py --input test.pyc --symbol symbols.txt

	the uncompile result is following. the code is unreadable.^^

	# 2018.07.09 14:31:02 DST
	#Embedded file name: @#6sGeSF3dK@
	import sys
	import os as myos
	
	def @0q9Fj3-XN4vcZg@(args = None, second_l = 'hhh'):
	    @n@-bSEBzqf89@ = 2
	    print @n@-bSEBzqf89@, args
	    lvar = 3
	
	    def @q(C2*4GW)Q!PF@():
	        print lvar, second_l
	
	    return @^+jeTJU&ORy#zg@
	
	
	class MyClass(object):
	
	    def @gTu^@$3Nh062*G@(self):
	        @mubZRLvHNG^@ = 123
	        self.id = @mubZRLvHNG^@
	
	    def @wC^U&#uvaHz1ifN@(self):
	        print self.id + 100
	
	
	myfunc(args='this is test args')()
	obj = MyClass()
	print obj.id
	obj.myfunc()
	print getattr(obj, 'myfunc')
	+++ okay decompyling test.pyc
	# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
	# 2018.07.09 14:31:02 DST


# more
	your can process a directory recursively.
	realxie$ python encrypt.py --input ./ --symbol symbols.txt


# symbols
	the symbols.txt is used to reconstruct debug messages.
