#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
from common import get_chart


CURRENT_FILE = Path(__file__).resolve().absolute()


qc = get_chart()
qc.to_file(f'{CURRENT_FILE}.png')
