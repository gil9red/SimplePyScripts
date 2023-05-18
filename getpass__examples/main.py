#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import getpass


# Return the “login name” of the user.
print("Hello,", getpass.getuser())

# NOTE: not work in PyCharm console
password = getpass.getpass()
print(password)

password = getpass.getpass("Input pass: ")
print(password)
