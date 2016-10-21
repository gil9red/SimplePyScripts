#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Парсер курса доллара и евро за текущую дату от сайта центробанка России."""


if __name__ == '__main__':
    from datetime import date
    date_req = date.today().strftime('%d.%m.%Y')
    url = 'https://www.cbr.ru/currency_base/daily.aspx?date_req=' + date_req

    from robobrowser import RoboBrowser
    browser = RoboBrowser(
        user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        parser='lxml'
    )
    browser.open(url)

    for tr in browser.select('.data tr'):
        td_list = tr.select('td')
        if not td_list:
            continue

        if td_list[1].text in ['USD', 'EUR']:
            print(td_list[1].text, td_list[4].text)
