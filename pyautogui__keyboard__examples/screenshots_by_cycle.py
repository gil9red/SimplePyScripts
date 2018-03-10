#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
from datetime import datetime
import pyautogui

DIR = 'screenshots'

import os
if not os.path.exists(DIR):
    os.mkdir(DIR)

while True:
    file_name = DIR + '/screenshot_{}.png'.format(datetime.now().strftime('%d%m%y %H%M%S'))
    im = pyautogui.screenshot(file_name)  # save file
    # print(im)

    time.sleep(1)
