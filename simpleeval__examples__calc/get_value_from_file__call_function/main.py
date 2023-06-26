#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install simpleeval
from simpleeval import SimpleEval


def get_from_file(file_name):
    with open(file_name) as f:
        return f.read()


my_eval = SimpleEval()
my_eval.functions["get"] = get_from_file

print(my_eval.eval("get('a_value.txt') + get('b_value.txt')"))  # '12345'
print(my_eval.eval("int(get('a_value.txt')) + int(get('b_value.txt'))"))  # 168
