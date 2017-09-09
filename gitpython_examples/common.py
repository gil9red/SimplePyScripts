#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


LOGIN = None
PASSWORD = None

# http://user:password@proxy_host:proxy_port
PROXY = None

if PROXY:
    import os
    os.environ['http_proxy'] = PROXY


NEW_REPO = 'Test-Repo'

import os
REPO_PATH = os.path.abspath(NEW_REPO)

# How use without input login and password:
# git clone https://username:password@github.com/username/repository.git
URL_GIT = 'https://{0}:{1}@github.com/{0}/{2}.git'.format(LOGIN, PASSWORD, NEW_REPO)


def get_repo():
    # pip install GitPython
    import git

    try:
        return git.Repo(REPO_PATH)

    except:
        return git.Repo.clone_from(URL_GIT, REPO_PATH)


def return_log(reverse=False):
    repo = get_repo()
    logs = repo.git.log('--pretty=format:%H%x09%an%x09%ad%x09%s').splitlines()

    if reverse:
        logs.reverse()

    return logs


def print_log(reverse=False):
    logs = return_log(reverse)
    print('Logs[{}]:'.format(len(logs)))

    for log in logs:
        print(log)
