#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_chart


qc = get_chart()
data = qc.get_bytes()
print(len(data))
# 13061
