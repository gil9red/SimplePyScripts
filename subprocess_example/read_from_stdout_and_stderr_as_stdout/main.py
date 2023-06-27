#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from subprocess import Popen, PIPE, STDOUT


rs = Popen(
    [sys.executable, "print_in_stdout_and_stderr.py"],
    universal_newlines=True,
    stdout=PIPE,
    stderr=STDOUT,
)
for line in rs.stdout:
    print(line.rstrip())
