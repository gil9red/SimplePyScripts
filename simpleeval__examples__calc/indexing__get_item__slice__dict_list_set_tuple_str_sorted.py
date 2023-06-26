#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install simpleeval
from simpleeval import SimpleEval


my_functions = {
    "dict": dict,
    "list": list,
    "set": set,
    "tuple": tuple,
    "str": str,
    "sorted": sorted,
}

my_eval = SimpleEval(functions=my_functions)

print(my_eval.eval('dict(a="1", b=2)["a"]'))  # "1"
print(my_eval.eval('list("123")[0]'))  # "1"
print(my_eval.eval('sorted(set("12213"))[0]'))  # "1"
print(my_eval.eval('tuple("123")[0]'))  # "1"
print(my_eval.eval("str(123)[0]"))  # "1"
print(my_eval.eval('sorted("43198")[0]'))  # "1"
print()

print(my_eval.eval('"1234567890"[:3]'))  # 123
print(my_eval.eval('list("1234567890")[:3]'))  # ['1', '2', '3']
print(my_eval.eval('"+".join(list("1234567890")[:3])'))  # 1+2+3
