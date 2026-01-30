#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from requests.adapters import HTTPAdapter


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, timeout, *args, **kwargs):
        self._timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, timeout=None, **kwargs):
        if timeout is None:
            timeout = self._timeout
        return super().send(request, timeout=timeout, **kwargs)


adapter = TimeoutHTTPAdapter(timeout=60)

session = requests.session()
session.mount('http://', adapter)
session.mount('https://', adapter)
session.headers["User-Agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
    "Gecko/20100101 Firefox/113.0"
)
