#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import sys

from logging.handlers import RotatingFileHandler

from example__cached import IGoUrl, GoUrl, GoUrlCachedProxy, requests


def get_logger(name, file="log.txt", encoding="utf-8"):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )

    # Simple file handler
    # fh = logging.FileHandler(file, encoding=encoding)
    # or:
    fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


class GoUrlLoggedProxy(IGoUrl):
    """Прокси"""

    _LOGGER = get_logger("GoUrlLoggedProxy")

    def __init__(self, go_url: IGoUrl = None):
        if go_url is None:
            go_url = GoUrl()

        self._url = go_url

    def get(self, url: str) -> requests.Response:
        self._log(f'Start get(url="{url}")')

        rs = self._url.get(url)
        self._log(f'Finish get(url="{url}") -> {rs}')

        return rs

    def get_status_code(self, url: str) -> int:
        self._log(f'Start get_status_code(url="{url}")')

        code = self._url.get_status_code(url)
        self._log(f'Finish get_status_code(url="{url}") -> {code}')

        return code

    def _log(self, text: str):
        GoUrlLoggedProxy._LOGGER.debug(text)


if __name__ == "__main__":
    import time

    class TimeThis:
        def __enter__(self):
            self.start_time = time.clock()
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            print("Elapsed time: {:.6f} sec".format(time.clock() - self.start_time))

    url = "https://github.com/gil9red"

    go_url = GoUrl()

    with TimeThis():
        rs = go_url.get(url)
        code = go_url.get_status_code(url)
        print(rs, rs.status_code, code, rs.content)

    print()
    print("Logged proxy:")

    go_url = GoUrlLoggedProxy()

    with TimeThis():
        rs = go_url.get(url)
        code = go_url.get_status_code(url)
        print(rs, rs.status_code, code, rs.content)

    print()
    print("Cached proxy with Logged proxy:")

    go_url = GoUrlLoggedProxy(go_url=GoUrlCachedProxy())

    with TimeThis():
        rs = go_url.get(url)
        code = go_url.get_status_code(url)
        print(rs, rs.status_code, code, rs.content)

    print()

    with TimeThis():
        rs = go_url.get(url)
        code = go_url.get_status_code(url)
        print(rs, rs.status_code, code, rs.content)
