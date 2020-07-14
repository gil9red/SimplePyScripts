#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/rootVIII/proxy_requests


# pip install proxy-requests
from proxy_requests import ProxyRequests


rs = ProxyRequests('https://api.ipify.org')
rs.get()
print(rs.get_raw())
# b'128.199.214.87'
