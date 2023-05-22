#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from html import unescape
from config import DIR_DUMP


for file_name in DIR_DUMP.glob("*/Описания иконы.txt"):
    text = file_name.read_text("utf-8")
    new_text = unescape(text)
    if text != new_text:
        print(file_name)
