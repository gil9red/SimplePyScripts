#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.request import urlopen
import json


def get_my_public_ip() -> str:
    with urlopen('http://jsonip.com/') as f:
        return json.loads(f.read())['ip']


if __name__ == '__main__':
    print(get_my_public_ip())
