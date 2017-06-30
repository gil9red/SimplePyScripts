#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


data = {
    'UserName': 'sidubi',
    'PassWord': 'sidubi@p33.org',
}

import requests
rs = requests.post('http://www.maultalk.com/ipb.html?act=Login&CODE=01', data=data)
print(rs)

# http://www.maultalk.com/ipb.html
print(rs.url)


from bs4 import BeautifulSoup
root = BeautifulSoup(rs.content, 'lxml')
print(root.select_one('#userlinks > p.home > b').text)  # Вошли как:  sidubi
