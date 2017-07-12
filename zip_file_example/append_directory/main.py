#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


DIR_NAME = 'dir_1'


if __name__ == '__main__':
    import zipfile
    with zipfile.ZipFile(DIR_NAME + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        import os
        for root, dirs, files in os.walk(DIR_NAME):
            for file in files:
                zf.write(os.path.join(root, file))
