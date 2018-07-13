#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


text = '"41", "1,234", "6,368,745", "12,34,567", "1234", "123,456"'

import re
print(re.findall(r'"(\d{,3}(?:,\d{3})*)"', text))  # ['41', '1,234', '6,368,745', '123,456']
