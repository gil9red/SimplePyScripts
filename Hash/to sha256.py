#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def to_sha256(text):
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()


if __name__ == '__main__':
    print(to_sha256('Hello World!'))
