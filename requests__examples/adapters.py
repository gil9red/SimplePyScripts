#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import urlparse
from random import randint

import requests
from requests.adapters import BaseAdapter, HTTPAdapter


class FileAdapter(BaseAdapter):
    def send(
        self,
        request: requests.PreparedRequest,
        stream: bool = False,
        timeout: None | float | tuple[float, float] | tuple[float, None] = None,
        verify: bool | str = True,
        cert: None | bytes | str | tuple[bytes | str, bytes | str] = None,
        proxies: dict[str, str] | None = None,
    ) -> requests.Response:
        file_name = urlparse(request.url).path

        rs = requests.Response()
        rs.status_code = 200
        rs.raw = open(file_name, "rb")
        rs.request = request

        return rs

    def close(self) -> None:
        pass


class DuckDuckGoAdapter(HTTPAdapter):
    def send(
        self,
        request: requests.PreparedRequest,
        stream: bool = False,
        timeout: None | float | tuple[float, float] | tuple[float, None] = None,
        verify: bool | str = True,
        cert: None | bytes | str | tuple[bytes | str, bytes | str] = None,
        proxies: dict[str, str] | None = None,
    ) -> requests.Response:
        query = urlparse(request.path_url).path

        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        return requests.get(url)  # TODO:


class RandomColorAdapter(BaseAdapter):
    def send(
        self,
        request: requests.PreparedRequest,
        stream: bool = False,
        timeout: None | float | tuple[float, float] | tuple[float, None] = None,
        verify: bool | str = True,
        cert: None | bytes | str | tuple[bytes | str, bytes | str] = None,
        proxies: dict[str, str] | None = None,
    ) -> requests.Response:
        r, g, b = map(
            lambda x: hex(x)[2:].zfill(2),
            (randint(0, 255), randint(0, 255), randint(0, 255)),
        )

        rs = requests.Response()
        rs.status_code = 200
        rs._content = f"#{r}{g}{b}".encode()
        rs.request = request

        return rs

    def close(self) -> None:
        pass


s = requests.session()
s.mount("file:", FileAdapter())
s.mount("duckduckgo:", DuckDuckGoAdapter())
s.mount("randomcolor:", RandomColorAdapter())

file_name = __file__
rs = s.get("file:" + file_name)
print(rs.content)
# b"#!/usr/bin/env python3\r\n# -*- coding: utf-8 -*-\r\n\r\n__author__ = 'ipetrash' ...

rs = s.get("duckduckgo:" + "Dark Souls")
print(rs.json())
# {'Abstract': "Dark Souls is a series of action role-playing games created by Hidet ...

rs = s.get("randomcolor:")
print(rs.content)
# b'#535ebd'
