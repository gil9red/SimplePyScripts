#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


LOGIN = None
PASSWORD = None

# http://user:password@proxy_host:proxy_port
PROXY = None

NEW_REPO = 'Test-Repo'

import os
REPO_PATH = os.path.abspath(NEW_REPO)

# How use without input login and password:
# git clone https://username:password@github.com/username/repository.git
URL_GIT = 'https://{0}:{1}@github.com/{0}/{2}.git'.format(LOGIN, PASSWORD, NEW_REPO)


if PROXY:
    import os
    os.environ['http_proxy'] = PROXY
