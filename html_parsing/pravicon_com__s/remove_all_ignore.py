#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from config import DIR_DUMP


for file_name in DIR_DUMP.glob('*/ignore'):
    file_name.unlink()
