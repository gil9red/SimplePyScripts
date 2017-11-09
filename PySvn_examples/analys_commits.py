#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/dsoprea/PySvn

def get_log_list() -> list:
    import svn.local
    repo = svn.local.LocalClient('E:/OPTT/optt_trunk')

    # OR:
    # import svn.remote
    # repo = svn.remote.RemoteClient('svn+cplus://svn2.compassplus.ru/twrbs/csm/optt/dev/trunk')

    return list(repo.log_default())


def get_log_list_by_author(log_list: list = None) -> dict:
    if not log_list:
        log_list = get_log_list()

    from collections import defaultdict
    author_by_log = defaultdict(list)

    for log in log_list:
        author_by_log[log.author].append(log)

    return author_by_log


if __name__ == '__main__':
    log_list = get_log_list()
    print('Total commits ({}):'.format(len(log_list)))

    author_by_log = get_log_list_by_author(log_list)

    for author, logs in sorted(author_by_log.items(), key=lambda item: len(item[1]), reverse=True):
        print('    {}: {}'.format(author, len(logs)))
