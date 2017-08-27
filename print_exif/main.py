#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Open image file for reading (binary mode)
f = open('exif_this.jpg', mode='rb')

# Return Exif tags
import exifread
tags = exifread.process_file(f)

if not tags:
    print('Not tags')
    quit()

print('Tags ({}):'.format(len(tags)))

for tag, value in tags.items():
    try:
        if value.field_type == 1:
            try:
                value = bytes(value.values).decode('utf-16')
            except:
                value = str(value.values)
        else:
            value = value.printable

    except:
        pass

    print('  "{}": {}'.format(tag, value))
