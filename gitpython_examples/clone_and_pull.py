#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


url = 'https://github.com/gil9red/search_in_users_github_gists.git'
# Если закончивается url на .git
len_url = len(url)
if '.git' == url[len_url - 4: len_url]:
    url = url[:len_url - 4]

import os

rw_dir = 'my_git_repos'
path = os.path.join(rw_dir, url.split('/')[-1])

# pip install gitpython
import git

if os.path.exists(path):
    repo = git.Repo(path)
else:
    repo = git.Repo.clone_from(url, path, branch='master')

# blast any current changes
repo.git.reset('--hard')

# ensure master is checked out
repo.heads.master.checkout()

# blast any changes there (only if it wasn't checked out)
repo.git.reset('--hard')

# remove any extra non-tracked files (.pyc, etc)
repo.git.clean('-xdf')

# pull in the changes from from the remote
repo.remotes.origin.pull()
