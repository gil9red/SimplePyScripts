#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


url = 'svn+cplus://svn2.compassplus.ru/twrbs/csm/optt/dev/trunk'

import svn.remote
repo = svn.remote.RemoteClient(url)

print(list(repo.log_default(revision_from=159807, limit=1)))
