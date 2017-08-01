#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def print_log(repo):
    logs = repo.git.log('--pretty=format:%H%x09%an%x09%ad%x09%s').splitlines()
    print('Logs[{}]:'.format(len(logs)))

    for log in logs:
        print(log)


if __name__ == '__main__':
    from config import get_repo
    repo = get_repo()

    print_log(repo)
