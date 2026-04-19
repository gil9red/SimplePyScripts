#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from requests.exceptions import RequestException


TIMEOUT: float = 60

session = requests.Session()


def do_get(url: str, **kwargs) -> requests.Response | None:
    timeout: float | None = kwargs.get("timeout")
    if timeout is None:
        kwargs["timeout"] = TIMEOUT

    exc: Exception | None = None
    for _ in range(5):
        try:
            return session.get(url, **kwargs)
        except RequestException as e:  # NOTE: Были ошибки сети
            exc = e

    if exc:
        raise exc


rs = do_get("https://httpbin.org/delay/1")
print(rs)

rs = do_get("https://httpbin.org/delay/2")
print(rs)

rs = do_get("https://httpbin.org/delay/3")
print(rs)
