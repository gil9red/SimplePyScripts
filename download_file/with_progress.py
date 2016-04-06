#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from urllib.request import urlretrieve


def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        if percent > 100:
            percent = 100
            readsofar = totalsize

        s = "\r%5.1f%% %*d / %d" % (percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")

    # total size is unknown
    else:
        sys.stderr.write("read %d\n" % (readsofar,))


if __name__ == '__main__':
    URL = 'https://github.com/gil9red/SimplePyScripts/archive/master.zip'

    local_filename, headers = urlretrieve(URL, reporthook=reporthook)
    print(local_filename + '\n' + headers)
