#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import uuid
from typing import List

import requests


URL_JSONRPC = 'https://nizhnekamsk.apigate.opencity.pro/api/jsonrpc'

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
session.headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJydS5nb3MtZGV2LmF1dGgiLCJpYXQiOjE2MDIxNzAwNzIsImV4cCI6MTAwMDE2MDIxNzAwNzEsInN1YiI6ImYxODIyMTMwLTI2OTctNDk5Ni1hNDExLWI4NzQwMzZlYjYxMyJ9.HmQJ5vL6fSzejEbEMzihDLDiwv86545JGuB3_MRlYe8'


def send_data(method: str, params: dict) -> dict:
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "id": str(uuid.uuid4()),
        "params": params,
    }
    rs = session.post(URL_JSONRPC, json=data)
    rs.raise_for_status()

    return rs.json()


def get_first_street_id(street_name: str) -> int:
    rs = send_data(
        "opencity.gis.street.index",
        {
            "limit": 20, "offset": 0,
            "filter": {"name": {"$like": f"%{street_name}%"}}
        }
    )
    return rs['result']['items'][0]['id']


def get_first_house_id(street_id: int, house_number: str) -> int:
    rs = send_data(
        "opencity.gis.house.index",
        {
            "filter": {"streetId": {"$eq": street_id}, "houseNumber": {"$like": f"{house_number}%"}},
            "limit": 0, "offset": 0,
            "sort": [{"field": "houseNumber", "desc": "ASC"}]
        }
    )
    return rs['result']['items'][0]['id']


def get_interrupts(house_id: int) -> List[dict]:
    rs = send_data(
        "opencity.interrupt.index",
        {
            "filter": {
                "houseId": {
                    "$eq": house_id
                }
            },
            "limit": 20, "offset": 0,
            "sort": [{"field": "dateStart", "desc": "DESC"}]
        }
    )
    return rs['result']['items']


if __name__ == '__main__':
    street_id = get_first_street_id('Ленина (Кармалы)')
    print(f'street_id: {street_id}')
    # street_id: 297

    house_id = get_first_house_id(street_id, '1')
    print(f'house_id: {house_id}')
    # house_id: 1978

    print()

    for item in get_interrupts(house_id):
        print(item['body'])
    """
    Эл/во (полностью). ВК-10кВ Ф-6 ПС Б.Толкиш отпайка на ктп 118 ,выборочная замена изоляторов,опора №58 установка траверсы на подвесных изоляторах. С 8-00 до 17-00  03/11/21  №9
    Эл/во (полностью). ВК-10кВ Ф-6 ПС Б.Толкиш отпайка на ктп 118 опора №9 выправка,установка траверсы на подвесных изоляторах,опоры №27,28 выправка. С 8-00 до 17-00  02/11/21  №9
    """