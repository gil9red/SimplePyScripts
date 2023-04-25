#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# from math import *
# print(eval("sin(10)*10**2"))
# print(eval("10**2"))
# print(eval("2+2*2"))
# print(eval("pow(64, 0.5)"))
# print(eval("64 ** 0.5"))
# print(eval("(2+2)*2"))
# print(eval("__import__('subprocess').Popen(['tasklist'],stdout=__import__('subprocess').PIPE).communicate()[0]"))
#
# import parser
# formula = "__import__('subprocess').Popen(['tasklist'],stdout=__import__('subprocess').PIPE).communicate()[0]"
# code = parser.expr(formula).compile()
# print(eval(code))


from numeric_string_parser import NumericStringParser


if __name__ == "__main__":
    nsp = NumericStringParser()
    print(nsp.eval("2^4"))
    print(nsp.eval("(2+2)*2^4"))
    print(nsp.eval("sin(2+2)"))
