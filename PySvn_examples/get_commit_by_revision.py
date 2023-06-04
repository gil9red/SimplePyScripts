#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import svn.remote
import config


repo = svn.remote.RemoteClient(config.URL_SVN)

print(list(repo.log_default(revision_from=159807, limit=1)))
