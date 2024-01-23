#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import functools
import time

import requests
from requests.exceptions import RequestException


def attempts(
    max_number: int = 5,
    sleep: int = 30,
    ignored_exceptions: tuple[type(Exception)] = (Exception,),
):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            number = 0
            while True:
                try:
                    print("\nGO", args, kwargs)
                    return func(*args, **kwargs)
                except Exception as e:
                    number += 1
                    print(f"ERROR on {number}/{max_number}: {e}")

                    if number >= max_number or not isinstance(e, ignored_exceptions):
                        raise e

                    print(f"Sleep {sleep} seconds")
                    time.sleep(sleep)

        return wrapped

    return actual_decorator


@attempts(
    max_number=3,
    sleep=5,
    ignored_exceptions=(RequestException,),
)
def do_get(url: str, *args, **kwargs) -> requests.Response:
    rs = requests.get(url, *args, **kwargs)
    rs.raise_for_status()

    return rs


print(do_get("https://google.com"))
"""
GO ('https://google.com',) {}
<Response [200]>
"""

print(do_get("http://sdfsdfs.dfsdf"))
"""
GO ('http://sdfsdfs.dfsdf',) {}
ERROR on 1/3: HTTPConnectionPool(host='sdfsdfs.dfsdf', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00000165C2C555D0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
Sleep 5 seconds

GO ('http://sdfsdfs.dfsdf',) {}
ERROR on 2/3: HTTPConnectionPool(host='sdfsdfs.dfsdf', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00000165C2C55D20>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
Sleep 5 seconds

GO ('http://sdfsdfs.dfsdf',) {}
ERROR on 3/3: HTTPConnectionPool(host='sdfsdfs.dfsdf', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00000165C2C56080>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
Traceback (most recent call last):
    ...
socket.gaierror: [Errno 11001] getaddrinfo failed

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
    ...
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPConnection object at 0x00000165C2C56080>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
    ...
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='sdfsdfs.dfsdf', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00000165C2C56080>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
    ...
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPConnectionPool(host='sdfsdfs.dfsdf', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00000165C2C56080>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
"""
