#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from subprocess import Popen, PIPE, STDOUT


args = ["python", "my_simple_calc.py"]

p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
p_stdout, p_stderr = p.communicate(input="1 2 3".encode())
print(p_stdout.decode())

p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
p_stdout, p_stderr = p.communicate(input="10 23".encode())
print(p_stdout.decode())

p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
p_stdout, p_stderr = p.communicate(input="10 23 7 8 9 abc".encode())
print(p_stdout.decode())
