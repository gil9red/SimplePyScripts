#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import config

import svn.remote
repo = svn.remote.RemoteClient(config.URL_SVN)

print(list(repo.log_default(revision_from=159807, limit=1)))
