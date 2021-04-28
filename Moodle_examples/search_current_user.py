#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import requests
from get_token import get_token


USERNAME = '<USERNAME>'
PASSWORD = '<PASSWORD>'


token = get_token(USERNAME, PASSWORD)

params = {
    'wstoken': token,
    'wsfunction': 'core_user_get_users_by_field',
    'moodlewsrestformat': 'json',
    'field': 'username',
    'values[0]': USERNAME,
}

rs = requests.get('http://newlms.magtu.ru/webservice/rest/server.php', params=params)
print(rs)

json_data = rs.json()
print('Response: {}'.format(json_data))

if 'errorcode' in json_data:
    print(json_data['errorcode'])
    sys.exit()

if not json_data:
    print('Not found user "{}"'.format(USERNAME))
    sys.exit()

info = json_data[0]
print(info['username'])
print(info['fullname'])
print(info['email'])
print(info['idnumber'])
