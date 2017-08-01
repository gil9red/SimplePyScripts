#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from config import REPO_PATH, URL_GIT


def get_repo():
    # pip install GitPython
    import git

    try:
        return git.Repo(REPO_PATH)

    except:
        return git.Repo.clone_from(URL_GIT, REPO_PATH)


def print_log(repo):
    logs = repo.git.log('--pretty=format:%H%x09%an%x09%ad%x09%s').splitlines()
    print('Logs[{}]:'.format(len(logs)))

    for log in logs:
        print(log)
