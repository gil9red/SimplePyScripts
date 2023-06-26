#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os


LOGIN = None
PASSWORD = None

# http://user:password@proxy_host:proxy_port
PROXY = None

NEW_REPO = "Test-Repo"
REPO_PATH = os.path.abspath(NEW_REPO)

# How use without input login and password:
# git clone https://username:password@github.com/username/repository.git
URL_GIT = f"https://{LOGIN}:{PASSWORD}@github.com/{LOGIN}/{NEW_REPO}.git"


if PROXY:
    os.environ["http_proxy"] = PROXY
