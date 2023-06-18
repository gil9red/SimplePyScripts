#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/847070/201445


import requests


def unshorten_url(url):
    return requests.head(url, allow_redirects=True).url


if __name__ == "__main__":
    url = "https://goo.gl/7RvxZh"
    print(unshorten_url(url))  # https://ru.stackoverflow.com/questions/847061/

    url = "https://bit.ly/2tHp17X"
    print(unshorten_url(url))  # https://ru.stackoverflow.com/questions/847061/
