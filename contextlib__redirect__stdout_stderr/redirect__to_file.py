#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from contextlib import redirect_stdout


# How to write help() to a file
with open("help.txt", "w") as f, redirect_stdout(f):
    help(pow)
