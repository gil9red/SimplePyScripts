#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


HTTP_HEADER_PATTERN = re.compile(r"([\w-]+): (.*)", flags=re.IGNORECASE)


def parse(text: str) -> dict[str, str]:
    return dict(HTTP_HEADER_PATTERN.findall(text))


if __name__ == "__main__":
    text_http_headers = """
    
    POST /index.php?do=search HTTP/1.1
    Host: online.anidub.com
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate, br
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 112
    Origin: https://online.anidub.com
    Connection: keep-alive
    Referer: https://online.anidub.com/index.php?do=search
    Upgrade-Insecure-Requests: 1
    TE: Trailers
    Pragma: no-cache
    Cache-Control: no-cache
    
    """

    headers = parse(text_http_headers)
    print(headers)
    assert headers == {
        "Host": "online.anidub.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "112",
        "Origin": "https://online.anidub.com",
        "Connection": "keep-alive",
        "Referer": "https://online.anidub.com/index.php?do=search",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
