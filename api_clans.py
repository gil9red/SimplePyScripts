#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import json

import requests


class Api:
    # TODO: this
    API_URL = "<HOST>/api_clans/1/index.php?request="

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

        self.session = requests.Session()
        self.session.headers["Authorization"] = self.make_authorization(login, password)
        # # Or:
        # self.session = requests.Session()
        # self.auth = (login, password)

    def method(self, method: str, data: dict = None) -> requests.Response:
        url = self.API_URL + method

        # Debug
        print(f"POST: url: {url}, data: {data}")

        rs = self.session.post(url, data)

        # Debug
        print(rs)
        print(f'rs.text: "{rs.text}"')
        print("pretty rs:", json.dumps(rs.json(), indent=4, ensure_ascii=False))
        print("\n")

        return rs

    def get_user_data(self, people_id=None) -> requests.Response:
        return self.method("get_user_data", {"people_id": people_id})

    # Append more api methods

    @staticmethod
    def make_authorization(login: str, password: str) -> str:
        credentials = login + ":" + password

        # As base64
        credentials = base64.b64encode(credentials.encode()).decode()

        return "Basic " + credentials


# # NOTE: Requests debug
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


if __name__ == "__main__":
    # TODO: this
    LOGIN = "<LOGIN>"
    PASSWORD = "<PASSWORD>"

    api = Api(LOGIN, PASSWORD)

    # Получение информации о текущем пользователе
    rs = api.get_user_data()
    # Or:
    rs = api.method("get_user_data")

    # Получение информации о пользователе с id = 1
    rs = api.get_user_data(people_id=1)
    # Or:
    rs = api.method("get_user_data", data={"people_id": 1})

    print("\n")

    # Создание пользователя
    data = {
        "name": "Вася",
        "lastname": "Пупкин",
        "secondname": "secondname",
        "sex": "man",
        "phone": "79957777555",
        "email": "guvuwer@p33.org",
        "pass": "123",
        "is_live": "1",
    }
    rs = api.method("add_user", data)
    new_user_id = rs.json()

    # Регистрация (Проверка кода подтверждения e-mail)
    rs = api.method("check_email_code", data={"people_id": new_user_id})
    email_code = rs.json()

    # Получение информации о новом пользователе с id = new_user_id
    rs = api.get_user_data(people_id=new_user_id)

    # # Получение связей пользователя с id = 1
    # data = {
    #     'people_id': 1,
    # }
    # rs = api.method('get_user_relations', data)
