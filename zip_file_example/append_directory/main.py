#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


DIR_NAME = 'dir_1'


import zipfile
with zipfile.ZipFile(DIR_NAME + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
    import os
    for root, dirs, files in os.walk(DIR_NAME):
        for file in files:
            file_name = os.path.join(root, file)
            zf.write(file_name)

            print(file_name)
