#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from contextlib import redirect_stdout


# How to send help() to stderr
with redirect_stdout(sys.stderr):
    help(dir)
