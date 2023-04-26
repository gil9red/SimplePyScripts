#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from io import StringIO
from contextlib import redirect_stdout


with StringIO() as f, redirect_stdout(f):
    print("Hello ", end="")

    def foo():
        print("World")

    foo()

    # Read from IO
    result = f.getvalue()

print(repr(result))  # 'Hello World\n'
