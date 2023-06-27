#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from subprocess import Popen, PIPE, STDOUT


p = Popen(["python", "google_search.py"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
p_stdout, p_stderr = p.communicate(input="Котики в чашке".encode())
print(p_stdout.decode())
