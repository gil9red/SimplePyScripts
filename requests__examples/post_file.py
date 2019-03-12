#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://docs.python-requests.org/en/master/user/quickstart/#post-a-multipart-encoded-file


import requests
from os.path import basename


url = 'https://httpbin.org/post'
abs_file_name = __file__
file_name = basename(abs_file_name)


files = {'file': open(abs_file_name, 'rb')}
rs = requests.post(url, files=files)
print(rs)
print(rs.text)
print()


# With file name
files = {'file': (abs_file_name, open(abs_file_name, 'rb'))}
rs = requests.post(url, files=files)
print(rs)
print(rs.text)
print()


# Send string as file
files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
rs = requests.post(url, files=files)
print(rs)
print(rs.text)


# Send bytes as file
files = {'file': ('report.csv', b'some,data,to,send\nanother,row,to,send\n')}
rs = requests.post(url, files=files)
print(rs)
print(rs.text)
