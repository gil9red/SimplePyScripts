#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


text = "in comparison to dogs, cats have not undergone major changes during the domestication process."

words = re.findall(r"\b(\w+)\b", text)
print(words)
