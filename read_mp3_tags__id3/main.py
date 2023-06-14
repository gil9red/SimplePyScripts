#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from mutagen.easyid3 import EasyID3


mp3info = EasyID3("test.mp3")

print(mp3info)
# {'artist': ['Foo'], 'title': ['Test'], 'album': ['Bar'], 'organization': ['Hello World']}
print()
print(mp3info["title"])  # ['Test']
print(mp3info["TITLE"])  # ['Test']
print()

# Print:
# artist: ['Foo']
# organization: ['Hello World']
# album: ['Bar']
# title: ['Test']
for k, v in mp3info.items():
    print("{}: {}".format(k, v))
