#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib
from datetime import datetime


ts = datetime.today().timestamp()
bts = str(ts).encode()

# Long
md5 = hashlib.md5()
md5.update(bts)

print(md5.hexdigest())

# Short
print(hashlib.md5(bts).hexdigest())
