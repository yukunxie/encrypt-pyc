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
	realxie$ ncompyle2 ./test/test.pyc
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
	realxie$ python encrypt.py --input ./test/test.pyc --symbol ./test/symbols.txt

	the uncompile result is following. the code is unreadable.^^

	```
	# 2018.07.09 14:52:57 DST
	#Embedded file name: @@xaBtIiWf6&hJq1@
	import sys
	import os as myos
	
	def @!FlsTUOG(i_+7BX@(args = None, second_l = 'hhh'):
	    @aV$eKzhIRLqEw@ = 2
	    print @aV$eKzhIRLqEw@, args
	    lvar = 3
	
	    def @@Bw&_l3)SC@():
	        print lvar, second_l
	
	    return @K1JX2ei&As76Vk)@
	
	
	class MyClass(object):
	
	    def @!8+CrKSDT0Pn@(self):
	        @it86I_4KyoF@ = 123
	        self.id = @it86I_4KyoF@
	
	    def @AhRcWgoO_S!@(self):
	        print self.id + 100
	
	
	myfunc(args='this is test args')()
	obj = MyClass()
	print obj.id
	obj.myfunc()
	print getattr(obj, 'myfunc')
	+++ okay decompyling test/test.pyc
	# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
	# 2018.07.09 14:52:57 DST
	```

# more
	your can process a directory recursively.
	realxie$ python encrypt.py --input ./test/ --symbol ./test/symbols.txt


# symbols
	the symbols.txt is used to reconstruct debug messages.
