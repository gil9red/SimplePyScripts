#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


if __name__ == '__main__':
    with open('_.torrent', 'rb') as f:
        torrent_file_bytes = f.read()
        torrent_file_text = torrent_file_bytes.decode('latin1')

    import effbot_bencode
    torrent = effbot_bencode.decode(torrent_file_text)

    total_size = 0

    print('Files:')
    for file in torrent["info"]["files"]:
        print("    %r - %d bytes" % ("/".join(file["path"]), file["length"]))

        total_size += file["length"]

    print()
    print("Total size: {} ({} bytes)".format(sizeof_fmt(total_size), total_size))
