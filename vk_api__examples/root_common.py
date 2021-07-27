#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging
import sys

import vk_api

from root_config import DIR, LOGIN, PASSWORD


def vk_auth(login: str, password: str) -> vk_api.VkApi:
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()

    return vk_session


def get_vk_session() -> vk_api.VkApi:
    return vk_auth(LOGIN, PASSWORD)


def get_logger(name, file=DIR / 'log.txt', encoding='utf8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s')

    if file:
        fh = logging.FileHandler(file, encoding=encoding)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log
