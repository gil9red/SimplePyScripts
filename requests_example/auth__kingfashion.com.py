#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# # NOTE: THIS DEBUG REQUESTS
# import logging
#
# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1
#
# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


if __name__ == '__main__':
    data = {
        'login[username]': 'yur4enko.vitya@yandex.ru',
        'login[password]': 'YEvbpUZ1i5LanIFnxfVW',
    }

    import requests
    session = requests.Session()

    rs = session.get('https://kingfashion.com/customer/account/')

    # Получение поля form_key из формы авторизации
    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')
    form_key = root.select_one('#login-form > input[name=form_key]')
    data['form_key'] = form_key['value']

    rs = session.post("https://kingfashion.com/customer/account/loginPost/", data=data)
    print(rs.url)

    root = BeautifulSoup(rs.content, 'lxml')
    print(root.select_one('.quick-access.shop > .account'))
