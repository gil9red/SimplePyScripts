#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_token(username, password):
    params = {
        'username': username,
        'password': password,
        'service': 'moodle_mobile_app',
    }
    import requests
    rs = requests.get('http://newlms.magtu.ru/login/token.php', params=params)
    print(rs)

    json_data = rs.json()
    print('Response: {}'.format(json_data))

    if 'errorcode' in json_data:
        print(json_data['errorcode'])
        return

    return json_data['token']


USERNAME = '<USERNAME>'
PASSWORD = '<PASSWORD>'

if __name__ == '__main__':
    token = get_token(USERNAME, PASSWORD)
    print('token: {}'.format(token))
