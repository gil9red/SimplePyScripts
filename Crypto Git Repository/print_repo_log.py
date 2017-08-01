#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import api
    repo = api.get_repo()

    api.print_log(repo)
