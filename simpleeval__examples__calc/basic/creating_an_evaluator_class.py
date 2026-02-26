#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/danthedeckie/simpleeval/blob/master/README.rst#creating-an-evaluator-class


# pip install simpleeval
from simpleeval import SimpleEval


# Evaluator class
my_eval = SimpleEval()
print(my_eval.eval("1 + 1"))  # 2
print(my_eval.eval("100 * 10"))  # 1000


# Append functions
def boo() -> str:
    return "Boo!"


my_eval.functions["boo"] = boo

# Set names
my_eval.names["fortytwo"] = 42
print(my_eval.eval("fortytwo * 4"))  # 168
print()


# this actually means you can modify names (or functions) with functions, if you really feel so inclined:
def set_val(name, value):
    my_eval.names[name] = value
    return value


my_eval.functions["set"] = set_val


print(my_eval.eval("set('age', 111)"))  # 111
print(my_eval.names)  # {..., 'age': 111}
print()

print(my_eval.eval("set('number', 777.777)"))  # 777.777
print(my_eval.names)  # {..., 'age': 111, 'number': 777.777}
print()

print(my_eval.eval("set('new_age', age * 11)"))  # 1221
print(my_eval.names)  # {..., 'age': 111, 'number': 777.777, 'new_age': 1221}
print()

print(my_eval.eval("set('age', age * age)"))  # 12321
print(my_eval.names)  # {..., 'age': 12321, 'number': 777.777, 'new_age': 1221}
