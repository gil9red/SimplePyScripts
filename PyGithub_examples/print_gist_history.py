#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from config import LOGIN, PASSWORD


if __name__ == '__main__':
    from github import Github
    gh = Github(LOGIN, PASSWORD)
    # gh = Github()

    gist = gh.get_gist('2f80a34fb601cd685353')
    print(gist)
    print('created_at: {}, updated_at: {}'.format(gist.created_at, gist.updated_at))
    print()

    print('files ({}): {}'.format(len(gist.files), gist.files))
    print()

    print('history ({}):'.format(len(gist.history)))

    # From new to old:
    # for history in gist.history:
    #
    # Or:
    # for history in reversed(gist.history):
    #
    # First 10:
    for history in list(reversed(gist.history))[:10]:
        print('    committed_at: {}, version: {}, files: {}'.format(
            history.committed_at, history.version, history.files)
        )

        file = history.files['gistfile1.txt']
        print('        url: {}'.format(file.raw_url))
        print('        [{}]: {}'.format(len(file.content), repr(file.content)[:150]))
        print()
