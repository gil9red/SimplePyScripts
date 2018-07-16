#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import cssselect
xpath_expr = cssselect.HTMLTranslator().css_to_xpath('div#main > a[href]')
print(xpath_expr)
