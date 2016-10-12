#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Если указывать свой логин и пароль, можно больше запросов делать в апи
LOGIN = None
PASSWORD = None

# http://user:password@proxy_host:proxy_port
PROXY = None

if PROXY:
    import os
    os.environ['http_proxy'] = PROXY

# TODO: сделать версию с gui

if __name__ == '__main__':
    from github import Github
    gh = Github(LOGIN, PASSWORD)

    # Без авторизации не получить секретные гисты
    gists = gh.get_user().get_gists()

    for i, gist in enumerate(gists, 1):
        print(i, gist.description, gist.html_url)

        for file, gist_file in gist.files.items():
            print('    ', file, gist_file.raw_url)

        print()
