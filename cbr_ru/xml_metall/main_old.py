#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path

# pip install matplotlib
import matplotlib.pyplot as plt

import requests

from bs4 import BeautifulSoup
from matplotlib import rcParams
from matplotlib.dates import DateFormatter


def gen_plot(dates, numbers, label=None, file_name="plot.png", show_plot=True):
    rcParams["font.family"] = "Times New Roman", "Arial", "Tahoma"
    rcParams["font.fantasy"] = "Times New Roman"
    rcParams["axes.labelsize"] = "large"
    rcParams["savefig.dpi"] = 200
    rcParams["axes.grid"] = True

    x_axis_date_formatter = DateFormatter("%d/%m/%y")

    # ax = plt.subplot(211)
    ax = plt.subplot(111)
    plt.plot(dates, numbers)
    # plt.plot(dates, numbers, 'ro-')
    # plt.fill_between(dates, numbers, color='r', alpha=0.7)

    plt.xlabel(label)
    ax.xaxis.set_major_formatter(x_axis_date_formatter)

    # ax = plt.subplot(212)
    # plt.plot(dates_list, number_users, 'go-')
    # plt.fill_between(dates_list, number_users, color='g', alpha=0.7)
    # plt.xlabel('Дата')
    # plt.ylabel('Количество пользователей')
    # ax.xaxis.set_major_formatter(x_axis_date_formatter)

    plt.savefig(file_name)

    if show_plot:
        plt.show()

    return file_name


if __name__ == "__main__":
    from datetime import date, datetime

    date_req1 = "01.01.2000"
    date_req2 = date.today().strftime("%d.%m.%Y")

    file_name = "metall_{}-{}.xml".format(date_req1, date_req2)

    # Кеширование. Если файла нет, то скачиваем его
    if not os.path.exists(file_name):
        url = "http://www.cbr.ru/scripts/xml_metall.asp?date_req1={}&date_req2={}".format(
            date_req1, date_req2
        )

        with open(file_name, "w") as f:
            rs = requests.get(url)
            f.write(rs.text)

    with open(file_name, "rb") as f:
        root = BeautifulSoup(f, "xml")

        # Code="1" -- Золото
        # Code="2" -- Серебро
        # Code="3" -- Платина
        # Code="4" -- Палладий
        records = root.find_all("Record", attrs=dict(Code="1"))

        dates = list()
        prices = list()

        for record in records:
            date = datetime.strptime(record["Date"], "%d.%m.%Y").date()
            price = float(record.findChild("Buy").text.replace(",", "."))

            dates.append(date)
            prices.append(price)

        # for i, record in enumerate(records, 1):
        for i, record in enumerate((records[0], records[-1]), 1):
            # b'<Record Date="06.01.2000" Code="1"><Buy>231,94</Buy><Sell>246,67</Sell></Record>\n\n'
            # record["Code"]
            print("{}. {}: {}".format(i, record["Date"], record.findChild("Buy").text))

        metall = root.findChild("Metall")
        from_date = datetime.strptime(metall["FromDate"], "%Y%m%d").strftime("%d.%m.%Y")
        to_date = datetime.strptime(metall["ToDate"], "%Y%m%d").strftime("%d.%m.%Y")
        gen_plot(
            dates,
            prices,
            "Стоимость грамма золота в рублях за {} - {}".format(from_date, to_date),
        )
