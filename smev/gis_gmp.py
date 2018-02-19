#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


data = open('example_rq.xml', 'rb').read()
url = 'http://smev-mvf.test.gosuslugi.ru:7777/gateway/services/SID0003663/wsdl'

import requests
rs = requests.post(url, data=data)
print(rs)

open('example_rs.xml', 'wb').write(rs.content)

from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'html.parser')
print(root.prettify())
