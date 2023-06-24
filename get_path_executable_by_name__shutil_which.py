#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3.7/library/shutil.html#shutil.which


import shutil


for name in ["python", "java", "cmd", "git", "svn"]:
    path = shutil.which(name)
    print("{:10} {}".format(name, path))
