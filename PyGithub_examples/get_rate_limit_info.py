#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from config import LOGIN, PASSWORD


if __name__ == '__main__':
    from github import Github
    gh = Github(LOGIN, PASSWORD)
    print('With auth:')
    print('  rate_limiting:', gh.rate_limiting)
    print('  rate_limiting_resettime:', gh.rate_limiting_resettime)
    print('  gh.get_rate_limit():', gh.get_rate_limit())
    print()

    gh = Github()
    print('Without auth:')
    print('  rate_limiting:', gh.rate_limiting)
    print('  rate_limiting_resettime:', gh.rate_limiting_resettime)
    print('  gh.get_rate_limit():', gh.get_rate_limit())
