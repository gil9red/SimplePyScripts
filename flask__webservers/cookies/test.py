#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests


session = requests.Session()


rs = session.get('http://127.0.0.1:5001/get-cookies')
print(rs, rs.url)
print(rs.headers)
print(rs.cookies)
print(rs.json())
"""
<Response [200]> http://127.0.0.1:5001/get-cookies
{'Content-Type': 'application/json', 'Content-Length': '3', 'Server': 'Werkzeug/0.15.4 Python/3.7.3', 'Date': 'Wed, 24 Feb 2021 13:28:00 GMT'}
<RequestsCookieJar[]>
{}
"""

print()

rs = session.post('http://127.0.0.1:5001/set-cookies', params=dict(a=123, b=3))
print(rs, rs.url)
print(rs.headers)
print(rs.cookies)
print(rs.json())
"""
<Response [200]> http://127.0.0.1:5001/set-cookies?a=123&b=3
{'Content-Type': 'application/json', 'Content-Length': '17', 'Set-Cookie': 'a=123; Path=/, b=3; Path=/', 'Server': 'Werkzeug/0.15.4 Python/3.7.3', 'Date': 'Wed, 24 Feb 2021 13:28:00 GMT'}
<RequestsCookieJar[<Cookie a=123 for 127.0.0.1/>, <Cookie b=3 for 127.0.0.1/>]>
{'ok': True}
"""

print()

rs = session.get('http://127.0.0.1:5001/get-cookies')
print(rs, rs.url)
print(rs.headers)
print(rs.cookies)
print(rs.json())
"""
<Response [200]> http://127.0.0.1:5001/get-cookies
{'Content-Type': 'application/json', 'Content-Length': '30', 'Server': 'Werkzeug/0.15.4 Python/3.7.3', 'Date': 'Wed, 24 Feb 2021 13:28:00 GMT'}
<RequestsCookieJar[]>
{'a': '123', 'b': '3'}
"""
