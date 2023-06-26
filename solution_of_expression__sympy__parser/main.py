#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)
from sympy import *


input_str = "(x+1)(y+1)+(x+1)y+xy"
transformations = standard_transformations + (implicit_multiplication_application,)
print(
    expand(parse_expr(input_str, transformations=transformations))
)
# 3*x*y + x + 2*y + 1
