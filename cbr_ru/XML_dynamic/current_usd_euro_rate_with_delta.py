#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import date, timedelta
from urllib.request import urlopen

from bs4 import BeautifulSoup


def current_rate(ccy_rq_id):
    """
    Функция возвращает кортеж из двух элементов: курс валюты и разница с предыдущим курсом.

    ccy_rq_id с значением "R01235" -- это USD

    :type ccy_rq_id: str
    """

    # Т.к. курс назначается не каждый день, разница может быть в несколько дней,
    # поэтому на всякий случай берем разницу от текущего дня и на 7 дней назад
    date_req1 = (date.today() - timedelta(days=7)).strftime("%d/%m/%Y")
    date_req2 = date.today().strftime("%d/%m/%Y")
    # date_req2 = (date.today() + timedelta(days=1)).strftime('%d/%m/%Y')

    url = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_req1}&date_req2={date_req2}&VAL_NM_RQ={ccy_rq_id}"

    with urlopen(url) as f:
        root = BeautifulSoup(f.read(), "xml")

        # Получаем список курсов
        values = root.select("Record > Value")
        if len(values) < 2:
            raise Exception(f"Что-то пошло не так. Не хватает значений.\nurl: {url}\nroot:\n{root}" )

        # Вытаскиваем последние два элемента и преобразуем в число
        values = [values[-2], values[-1]]
        values = [float(price.text.replace(",", ".")) for price in values]

        delta = values[1] - values[0]
        return values[1], delta


if __name__ == "__main__":
    # R01235 -- USD, доллары, 840
    price, delta = current_rate("R01235")
    print(f"USD: {price} ({('+' if delta > 0 else '')}{delta:.4f})")

    # R01239 -- EUR, евро, 978
    price, delta = current_rate("R01239")
    print(f"EUR: {price} ({('+' if delta > 0 else '')}{delta:.4f})")
