#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time

from fb2_pictures import do as do1
from fb2_pictures_using_re import do as do2


file_name = 'Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2'
count = 25


if __name__ == '__main__':
    # Xml быстрее Re

    t = time.clock()
    for i in range(count):
        do1(file_name, False)
    print('Xml: {:.2f} sec'.format(time.clock() - t))

    t = time.clock()
    for i in range(count):
        do2(file_name, False)
    print('Re: {:.2f} sec'.format(time.clock() - t))
