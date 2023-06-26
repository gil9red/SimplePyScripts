#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/danthedeckie/simpleeval/blob/master/README.rst#names


# pip install simpleeval
from simpleeval import simple_eval, SimpleEval


print(simple_eval("a + b", names={"a": 11, "b": 100}))  # 111
print(simple_eval("a + b * 2", names={"a": 2, "b": 2}))  # 6
print(simple_eval("a + b * 2", names=dict(a=2, b=2)))  # 6
print()


# Hand the handling of names over to a function
def name_handler(node):
    return ord(node.id.lower()) - 96


# a -- 1, b -- 2, c -- 3
print(simple_eval("A + b + c", names=name_handler))  # 6


# Hand the handling of names over to a function
def name_handler_dict(node):
    name_by_value = {
        "a": 100,
        "b": 10,
        "c": 1,
    }

    name = node.id.lower()
    return name_by_value[name]


print(simple_eval("A + b + c", names=name_handler_dict))  # 111
print()


# SimpleEval class

my_eval = SimpleEval()
my_eval.names["a"] = 1
my_eval.names["b"] = 1

print(my_eval.eval("a + b"))  # 2

try:
    print(my_eval.eval("a + b + c"))
except Exception as e:
    print(e)  # 'c' is not defined for expression 'a + b + c'

my_eval.names["c"] = 3
print(my_eval.eval("a + b + c"))  # 5
