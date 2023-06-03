#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install PyMsgBox
from pymsgbox import confirm


button = confirm(text="My Text", title="My Title", buttons=["OK", "Cancel"])
print(button)
