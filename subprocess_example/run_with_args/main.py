#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from subprocess import Popen, PIPE


program = "python"
process = Popen([program, "my_calc.py", "123", "+", "456"], stdout=PIPE, shell=True)
print(process.communicate()[0].strip())
# b'579.0'

# NOTE: Wrong! Arguments must be passed separately
# process = Popen([program, 'my_calc.py', '123 + 456'], stdout=PIPE, shell=True)
# print(process.communicate()[0].strip())
