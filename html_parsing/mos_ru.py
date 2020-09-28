#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

post_url = 'https://www.mos.ru/'
rs = session.get(post_url)
print("mos.ru status:", rs.status_code)

auth_url = 'https://www.mos.ru/api/acs/v1/login?back_url=https%3A%2F%2Fwww.mos.ru%2F'
rs = session.get(auth_url)
print("login.mos.ru status:", rs.status_code)

root = BeautifulSoup(rs.content, 'html.parser')

csrf_token = root.select_one('meta[name=csrf-token-value]')
print(csrf_token['content'])
# 16390112a86ceaae4559cac6c9e23b43ffaf99aecbc54ed84fcb0aa0af43ff03e29a522066398f0f
