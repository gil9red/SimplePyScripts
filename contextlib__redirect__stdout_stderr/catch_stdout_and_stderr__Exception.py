#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from contextlib import redirect_stdout, redirect_stderr
import io
import sys
import traceback


f = io.StringIO()

with redirect_stdout(f), redirect_stderr(f):
    try:
        print("123")
        print("abc")
        1 / 0
    except:
        print(traceback.format_exc(), file=sys.stderr)

s = f.getvalue()
print(s)
# 123
# abc
# Traceback (most recent call last):
#   File ..., line 18, in <module>
#     1 / 0
# ZeroDivisionError: division by zero
