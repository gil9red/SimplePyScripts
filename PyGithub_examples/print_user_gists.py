#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from config import LOGIN, PASSWORD

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
