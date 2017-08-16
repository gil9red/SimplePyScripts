#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


USERNAME = '<USERNAME>'
PASSWORD = '<PASSWORD>'


if __name__ == '__main__':
    from get_token import get_token
    token = get_token(USERNAME, PASSWORD)

    params = {
        'wstoken': token,
        'wsfunction': 'core_user_get_users_by_field',
        'moodlewsrestformat': 'json',
        'field': 'username',
        'values[0]': USERNAME,
    }

    import requests
    rs = requests.get('http://newlms.magtu.ru/webservice/rest/server.php', params=params)
    print(rs)

    json_data = rs.json()
    print('Response: {}'.format(json_data))

    if 'errorcode' in json_data:
        print(json_data['errorcode'])
        quit()

    if not json_data:
        print('Not found user "{}"'.format(USERNAME))
        quit()

    info = json_data[0]
    print(info['username'])
    print(info['fullname'])
    print(info['email'])
    print(info['idnumber'])
