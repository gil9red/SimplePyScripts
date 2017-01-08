#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime
import hashlib 


if __name__ == '__main__':
    ts = datetime.today().timestamp()
    bts = str(ts).encode()

    # Long
    md5 = hashlib.md5()
    md5.update(bts)

    print(md5.hexdigest())

    # Short
    print(hashlib.md5(bts).hexdigest())

