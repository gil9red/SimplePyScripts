#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent))
from human_byte_size import sizeof_fmt
