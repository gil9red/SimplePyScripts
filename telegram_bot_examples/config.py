#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os


TOKEN = os.environ.get('TOKEN') or open('TOKEN.txt', encoding='utf-8').read().strip()

ERROR_TEXT = '⚠ Возникла какая-то проблема. Попробуйте повторить запрос или попробовать чуть позже...'
