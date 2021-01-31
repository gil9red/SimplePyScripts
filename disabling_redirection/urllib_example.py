#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import urllib.request


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        return fp

    http_error_302 = http_error_303 = http_error_307 = http_error_301


rs = urllib.request.urlopen('http://ya.ru/')
print(rs.code, rs.url)
# 200 https://ya.ru/

opener = urllib.request.build_opener(NoRedirectHandler())
urllib.request.install_opener(opener)

rs = urllib.request.urlopen('http://ya.ru/')
print(rs.code, rs.url)
# 302 http://ya.ru/
