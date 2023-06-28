#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install humanize
from humanize import naturalsize as sizeof_fmt

import effbot_bencode


with open("_.torrent", "rb") as f:
    torrent_file_bytes = f.read()
    torrent_file_text = torrent_file_bytes.decode("latin1")

torrent = effbot_bencode.decode(torrent_file_text)
total_size = 0

print("Files:")
for file in torrent["info"]["files"]:
    print(f"    {'/'.join(file['path'])!r} - {file['length']:d} bytes")
    total_size += file["length"]

print()
print(f"Total size: {sizeof_fmt(total_size)} ({total_size} bytes)")
