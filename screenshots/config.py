#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path


DIR = Path(__file__).parent.resolve()
DIR_OUTPUT = DIR / 'output'

DIR_OUTPUT.mkdir(exist_ok=True)
