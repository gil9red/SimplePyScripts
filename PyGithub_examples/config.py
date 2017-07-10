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
