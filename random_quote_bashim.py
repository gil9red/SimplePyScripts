#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


url = 'http://bash.im/random'

from lxml import etree
from urllib.request import urlopen, Request

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'

with urlopen(Request(url, headers={'User-Agent': USER_AGENT})) as f:
    root = etree.HTML(f.read())

    quote_el = root.cssselect('.quote')[0]
    text_el = root.cssselect('.text')[0]

    from urllib.parse import urljoin
    print(urljoin(url, root.cssselect('.id')[0].attrib['href']))
    print()

    # По умолчанию, lxml работает с байтами и по умолчанию считает, что работает с ISO8859-1 (latin-1)
    # а на баше кодировка страниц cp1251, поэтому сначала нужно текст раскодировать в байты,
    # а потом закодировать как cp1251
    quote_text = '\n'.join([text.encode('ISO8859-1').decode('cp1251') for text in text_el.itertext()])
    print(quote_text)
