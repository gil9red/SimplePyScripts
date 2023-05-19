#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_repo


repo = get_repo()
urls = list(repo.remotes.origin.urls)
print(f'Urls ({len(urls)}):')
for url in urls:
    print(f'    {url}')
