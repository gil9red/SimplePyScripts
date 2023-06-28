#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import effbot_bencode
import another_bencode
import bencode_py3


with open("_.torrent", "rb") as f:
    torrent_file_bytes = f.read()
    torrent_file_text = torrent_file_bytes.decode("latin1")

torrent = effbot_bencode.decode(torrent_file_text)
print("effbot_bencode:")
print(f"    {torrent}")
print("    Files:")
for file in torrent["info"]["files"]:
    print(f"        {'/'.join(file['path'])!r} - {file['length']:d} bytes")

print("\n")
torrent = another_bencode.decode(torrent_file_bytes)[0]
print("another_bencode:")
print(f"    {torrent}")
print("    Files:")
for file in torrent[b"info"][b"files"]:
    print(
        f"        {b'/'.join(file[b'path']).decode('utf-8')!r} - {file[b'length']:d} bytes"
    )

print("\n")
torrent = bencode_py3.bdecode(torrent_file_text)
print("bencode_py3:")
print(f"    {torrent}")
print("    Files:")
for file in torrent["info"]["files"]:
    print(f"        {'/'.join(file['path'])!r} - {file['length']:d} bytes")
