#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import os.path
import sys
import time

from PySide.QtGui import *
from PySide.QtCore import *


def get_logger(name, file='log.txt', encoding='utf8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


logger = get_logger('dir_sizes')


def get_bytes(text, units='BKMGTPE'):
    """Возвращает числовое значение в байтах разбирая строки вида: 1 GB, 50 MB и т.п."""

    text = text.strip().replace(' ', '').replace(',', '.')

    # For '54,7GB' -> num='54,7' and unit='G'
    num, unit = float(text[:-2]), text[-2:][0]
    assert len(unit) == 1, 'Len unit should == 1, example G, M. Unit = {}.'.format(unit)
    assert unit in units, 'Unknows unit {}, possible: {}.'.format(unit, ', '.join(tuple(units)))

    unit_pow = units.find(unit)
    assert unit_pow > 0, 'Unit pow should > 0, unit_pow={} unit={}.'.format(unit_pow, unit)

    return int(num * 1024 ** unit_pow)


def pretty_file_size(n_size):
    i = 0
    size = n_size

    while size >= 1024:
        size /= 1024
        i += 1

    return n_size, '{:.2f}'.format(size) + ' ' + "BKMGTPE"[i] + 'B'


def dir_size_bytes(dir_path, files=0, dirs=0, level=0, do_indent=True, size_less=get_bytes('1 GB')):
    it = QDirIterator(dir_path, '*.*', QDir.AllEntries | QDir.NoDotAndDotDot | QDir.Hidden | QDir.System)

    sizes = 0

    while it.hasNext():
        file_name = it.next()
        file = QFileInfo(file_name)

        if file.isDir():
            dirs += 1
            size, files, dirs = dir_size_bytes(file_name, files, dirs, level + 1, do_indent, size_less)
        else:
            files += 1
            size = file.size()

        sizes += size

    if sizes > size_less:
        logger.debug(
            ((' ' * 4 * level) if do_indent else '')
            + os.path.normpath(dir_path) + ' ' + '{1} ({0} bytes)'.format(*pretty_file_size(sizes))
        )

    return sizes, files, dirs


if __name__ == '__main__':
    app = QApplication(sys.argv)

    dir_name = r"C:\\"

    t = time.clock()
    sizes, files, dirs = dir_size_bytes(dir_name, do_indent=False, size_less=get_bytes('2GB'))

    logger.debug('\nsizes = {}, files = {}, dirs = {}'.format('{1} ({0} bytes)'.format(*pretty_file_size(sizes)), files, dirs))
    logger.debug('{:.2f} sec'.format(time.clock() - t))
