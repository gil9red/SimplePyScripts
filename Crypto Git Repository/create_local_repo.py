#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from config import get_repo
    repo = get_repo()

    print('Repo:', repo)
    print()

    from print_repo_log import print_log
    print_log(repo)
