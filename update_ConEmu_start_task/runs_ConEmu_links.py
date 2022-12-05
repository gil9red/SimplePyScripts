#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
from config import DIR_STARTUP, PREFIX_LINK


for f in DIR_STARTUP.glob(f'{PREFIX_LINK}*.lnk'):
    print(f'Run "{f}"')
    os.startfile(f)
