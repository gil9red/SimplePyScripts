#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


text = open('Syslog.txt').read()

import re
for mac in set(re.findall(r'[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}', text)):
    print(mac)
