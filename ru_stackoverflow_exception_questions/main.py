#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт добавляет метку 'исключения' для указанных вопросов."""


def get_logger(name, file='log.txt', encoding='utf8'):
    import logging
    import sys

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    fh = logging.FileHandler(file, encoding=encoding)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)
    return log


logger = get_logger('so_questions')


import json
config = json.load(open('config', encoding='utf8'))
LOGIN = config['login']
PASSWORD = config['password']

#
# import time
# import traceback


from gatherer import query

if __name__ == '__main__':
    print(query.all()[17].url)
    print(query.count())
    # print(query.all())
    quit()
