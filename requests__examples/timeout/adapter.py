#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from requests.adapters import HTTPAdapter


class TimeoutHttpAdapter(HTTPAdapter):
    def __init__(self, timeout, *args, **kwargs) -> None:
        self._timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, timeout=None, **kwargs):
        if timeout is None:
            timeout = self._timeout
        return super().send(request, timeout=timeout, **kwargs)


adapter = TimeoutHttpAdapter(timeout=60)

session = requests.session()
session.mount("http://", adapter)
session.mount("https://", adapter)


rs = session.get("https://httpbin.org/delay/1")
print(rs)

rs = session.get("https://httpbin.org/delay/2")
print(rs)

rs = session.get("https://httpbin.org/delay/3")
print(rs)
