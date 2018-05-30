#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = 'in comparison to dogs, cats have not undergone major changes during the domestication process.'

import re
words = re.findall(r'\b(\w+)\b', text)
print(words)
