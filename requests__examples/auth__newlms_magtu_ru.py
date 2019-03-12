#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'


if __name__ == '__main__':
    import requests
    session = requests.session()

    rs = session.post('http://newlms.magtu.ru/login/index.php', data={'username': LOGIN, 'password': PASSWORD})
    print(rs)

    # Если логин / пароль правильный, случится переход на главную страницу
    success = rs.url == 'http://newlms.magtu.ru/'
    print(success)

    if success:
        from bs4 import BeautifulSoup
        root = BeautifulSoup(rs.content, 'lxml')

        print('Меню:')
        for a in root.select('a.menu-action'):
            print('    {} -> {}'.format(a.text, a['href']))
