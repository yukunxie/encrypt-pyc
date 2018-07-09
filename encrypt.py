# -*- coding: utf-8 -*-
'''
*** Date        :    2018-07-09 13:24:39
*** Author        :     realxie/解玉坤
*** Email         :     jinyun2007@126.com
*** Description    :     replace local variable name with unreadable names / 对编译后的pyc文件进行加密，
***                    将pyc中的局部变量名称进行不可读替换，使得反编译后的py文件无法执行
*** Version     :    for python27
'''
import dis
import marshal
import struct
import sys
import os
import time
import types
import random


def gen_random_symbol(symbol_dict, key):
    if key.startswith("@@"):
        return key
    if key in symbol_dict:
        return symbol_dict[key]
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    while 1:
        value = "@@" + "".join(random.sample(seed, random.randint(10,15)))
        if value not in symbol_dict:
            symbol_dict[key] = value
            symbol_dict[value] = key
            return value

def load_symbol_file(filename):
    symbol_dict = {}
    if not os.path.exists(filename):
        return symbol_dict

    with open(filename, "r") as fd:
        for text in fd.readlines():
            text = text.replace("\n", "")
            if not text:
                continue
            (key, value) = text.split(" ")
            symbol_dict[key] = value
            symbol_dict[value] = key
    return symbol_dict

def save_symbol_file(filename, symbol_dict):
    with open(filename, "w") as fd:
        fd.truncate(0)
        for k, v in symbol_dict.iteritems():
            if k.startswith("@@"):
                continue
            fd.write("%s %s\n" % (v, k))
        fd.close()



def process_file(fname, symbol_dict):
    with open(fname, "rb") as f:
        magic = f.read(4)
        moddate = f.read(4)
        code = marshal.load(f)

    new_code = gen_new_code(code, symbol_dict)

    with open(fname, "wb") as fd:
        fd.truncate(0)
        data = magic + moddate + marshal.dumps(new_code)
        fd.write(data)
     
def gen_new_code(code, symbol_dict):
    varnames = []
    for i, varname in enumerate(code.co_varnames):
        # skip function arguments
        if i < code.co_argcount:
            varnames.append(varname)
        else:
            varnames.append(gen_random_symbol(symbol_dict, varname))
    varnames = tuple(varnames)

    consts = []
    for const in code.co_consts:
        if type(const) == types.CodeType:
            new_code = gen_new_code(const, symbol_dict)
            consts.append(new_code)
        else:
            consts.append(const)
    consts = tuple(consts)

    opt_code = types.CodeType(code.co_argcount,
                             code.co_nlocals,
                             code.co_stacksize,
                             code.co_flags,
                             code.co_code,      # code.co_code: this you changed
                             consts,             #code.co_consts,
                             code.co_names,
                             varnames,            #code.co_varnames,
                             code.co_filename,
                             code.co_name,
                             code.co_firstlineno,
                             code.co_lnotab,       # In general, You should adjust this
                             code.co_freevars,
                             code.co_cellvars)
    return opt_code

symbol_dict = load_symbol_file("symbols.txt")
process_file(sys.argv[1], symbol_dict) 
save_symbol_file("symbols.txt", symbol_dict)
