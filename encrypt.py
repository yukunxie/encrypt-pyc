# -*- coding: utf-8 -*-
'''
# Date         :  2018-07-09 13:24:39
# Author       :  realxie/解玉坤
# Email        :  jinyun2007@126.com
# Description  :  replace local variable name with unreadable names / 对编译后的pyc文件进行加密，
#                  将pyc中的局部变量名称进行不可读替换，使得反编译后的py文件无法执行
# Version      :  for python27
'''
import dis
import marshal
import struct
import sys
import os
import time
import types
import random
import argparse

random.seed(int(time.time()))


'''
# generate a new random name even for a same key
# while, you can gen a same name for same key, optionally.
'''
USE_UNIQUE_VARNAME = False

def gen_random_symbol(symbol_dict, key):
    if key.startswith("@@"):
        return key
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%^&*()_+=-"

    if USE_UNIQUE_VARNAME and (key in symbol_dict):
        return symbol_dict[key]

    # gen short random name
    for i in xrange(100):
        value = "@" + "".join(random.sample(seed, random.randint(10,15))) + "@"
        if value not in symbol_dict:
            symbol_dict[value] = key
            if USE_UNIQUE_VARNAME:
                symbol_dict[key] = value
            return value

    # gen a long random name
    while 1:
        value = "@" + "".join(random.sample(seed, random.randint(16,25))) + "@"
        if value not in symbol_dict:
            symbol_dict[value] = key
            if USE_UNIQUE_VARNAME:
                symbol_dict[key] = value
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
            if k.startswith("@"):
                fd.write("%s %s\n" % (k, v))
        fd.close()

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
                             gen_random_symbol(symbol_dict, code.co_filename), #code.co_filename,
                             gen_random_symbol(symbol_dict, code.co_name),#code.co_name,
                             code.co_firstlineno,
                             code.co_lnotab,       # In general, You should adjust this
                             code.co_freevars,
                             code.co_cellvars)
    return opt_code

'''
*** get all files with special suffix in root_dir
'''
def get_all_files(root_dir, suffix = []):
    ret = []
    for root, dirs, files in os.walk(root_dir):
        if root.find(".svn") >= 0:
            continue
        for file in files:
            if not suffix:
                ret.append(os.path.join(root,file))
            else:
                base, suf = os.path.splitext(file)
                if suf in suffix:
                    ret.append(os.path.join(root,file))
    return ret


def process_file(fname, symbol_dict):
    print ">>> process file:", fname
    with open(fname, "rb") as f:
        magic = f.read(4)
        moddate = f.read(4)
        code = marshal.load(f)
    new_code = gen_new_code(code, symbol_dict)
    with open(fname, "wb") as fd:
        fd.truncate(0)
        data = magic + moddate + marshal.dumps(new_code)
        fd.write(data)

def process_dir(fdir, symbol_dict):
    for file in get_all_files(fdir, [".pyc"]):
        process_file(file, symbol_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='encrypt pyc files.\npowered by realxie.')
    parser.add_argument('--input', help='the target pyc or direcotry')
    parser.add_argument('--symbol', help='the symbols file path')
    parser.add_argument('--unique', help='whether use the unique random name for a same variable name(True/False, default is False)')
    args = parser.parse_args()

    USE_UNIQUE_VARNAME = (args.unique != None) and bool(args.unique.lower() in ["true", "1"])

    symbol_dict = load_symbol_file(args.symbol)
    if os.path.isdir(args.input):
        process_dir(args.input, symbol_dict)
    else:
        process_file(args.input, symbol_dict)
    save_symbol_file( args.symbol, symbol_dict)

    print "done."

