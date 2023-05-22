#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/questions/953820/


import re
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


def get_csrfmiddlewaretoken(rs) -> str:
    match = re.search("csrfmiddlewaretoken: '(.+?)',", rs.text)
    if match:
        return match.group(1)


COMMON_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0",
}


with requests.Session() as s:
    rs = s.get("https://lk.ugatu.su/raspisanie/", headers=COMMON_HEADERS)
    print(rs)

    csrfmiddlewaretoken = get_csrfmiddlewaretoken(rs)

    # Эмуляция клика на кнопку "ПОКАЗАТЬ"
    data = {
        "csrfmiddlewaretoken": csrfmiddlewaretoken,
        "faculty": "АВИЭТ",
        "klass": "1",
        "group": "2435",
        "ScheduleType": "За+неделю",
        "week": "5",
        "date": "07.03.2019",
        "sem": "9",
        "view": "ПОКАЗАТЬ",
    }
    # Костыль для обхода проблемы составления ScheduleType='За+неделю'
    # Дело в том, что если в data положить словарь, то 'За+неделю' будет закодирован как
    # '%D0%97%D0%B0%2B%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D1%8E'
    # а браузер кодирует как '%D0%97%D0%B0+%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D1%8E', т.е.
    # символ '+' должен оставаться собой. Если плюс закодировать, сервер вернет пустую таблицу
    #
    # NOTE: возможно, лучше вместо костыля с urlencode+replace вручную собрать строку
    #
    data = urlencode(data).replace("%2B", "+").encode()

    headers = {
        "Referer": "https://lk.ugatu.su/raspisanie/",
        # Нужно заполнить, т.к. в post data передан не как словарь
        "Content-Type": "application/x-www-form-urlencoded",
    }
    headers.update(COMMON_HEADERS)

    rs = s.post("https://lk.ugatu.su/raspisanie/", data=data, headers=headers)

    root = BeautifulSoup(rs.content, "html.parser")
    print(root.select_one("#schedule .bgc-lecture-practical"))

# Консоль:
# <Response [200]>
# <Response [200]>
# <td class="bgc-lecture-practical"><p><font class="font-subject">Современные проблемы биомедицинской и экологической инженерии</font><br/><font class="font-classroom"><a href="#" onclick="return false" onmouseup="GoToTheLink(1, 3, 128)">4-324</a></font><font class="font-teacher"><p>Лекция + практика</p><a href="#" onclick="return false" onmouseup="GoToTheLink(1, 2, 50126)">Демин Алексей Юрьевич</a></font></p></td>
