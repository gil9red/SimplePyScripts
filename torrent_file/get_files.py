#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    with open('_.torrent', 'rb') as f:
        torrent_file_bytes = f.read()
        torrent_file_text = torrent_file_bytes.decode('latin1')

    import effbot_bencode
    torrent = effbot_bencode.decode(torrent_file_text)
    print('effbot_bencode:')
    print('    {}'.format(torrent))
    print('    Files:')
    for file in torrent["info"]["files"]:
        print("        %r - %d bytes" % ("/".join(file["path"]), file["length"]))

    print('\n')
    import another_bencode
    torrent = another_bencode.decode(torrent_file_bytes)[0]
    print('another_bencode:')
    print('    {}'.format(torrent))
    print('    Files:')
    for file in torrent[b"info"][b"files"]:
        print("        %r - %d bytes" % (b"/".join(file[b"path"]), file[b"length"]))

    print('\n')
    import bencode_py3
    torrent = bencode_py3.bdecode(torrent_file_text)
    print('bencode_py3:')
    print('    {}'.format(torrent))
    print('    Files:')
    for file in torrent["info"]["files"]:
        print("        %r - %d bytes" % ("/".join(file["path"]), file["length"]))
