#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
На сайте doska.ru после клика на "Показать телефон" и ввода капчи приходит зашифрованная команда,
в которой спрятан номер(ы) телефонов без кодов операторов

Скрипт расшифровывает команду и возвращает номера. Но такие номера бесполезны без страницы с которой
команда была получена:
На странице например было: +7(905)**-***-**
Пришла команда с номером и ее разобрало как ['-00-00', '11-822-14', '-00-00']
Т.е. телефон на самом деле был +7(905)11-822-14 (телефон случайный, а не с сайта)


SOURCE: http://www.prog.org.ru/index.php?topic=31490.msg232893#msg232893

"""


import re
from base64 import b64decode


def _ph_dec(g, r, k):
    decode_base64 = b64decode(g).decode("utf-8")
    g = re.sub(r"%([a-fA-F0-9]{2})", lambda m: chr(int(m.group(1), 16)), decode_base64)

    n = len(r)
    d = len(g)
    c = ""
    f = 0

    while f < d:
        q = g[f : f + 1]
        p = r[f % n : f % n + 1]

        if k == 1:
            q = ord(q[0]) - ord(p[0])
        else:
            if k == 2:
                q = ord(q[0]) - ord(p[0]) + 14
            else:
                q = ord(q[0]) ^ ord(p[0])

        c = c + chr(q)
        f += 1

    return c


def gpzd(data, key):
    key = int(key)

    key = key * 6 - 47289 + 517
    return _ph_dec(data, str(key), 2)


def get_phones_from_command(cmd):
    phones = list()

    cmd = cmd.split("\t")
    for i in cmd:
        data = i.split("|")

        b = gpzd(data[1], data[2])
        phone = _ph_dec(b, "K0dbVwzGrpLa-wRs2", 2)
        phones.append(phone)

    return phones


if __name__ == "__main__":
    cmd = (
        "1|JTg0JTkxbyU5NnVqJTdDJThGc2drWnR6JTkxWA==|22481814	"
        "2|JTg1JTk3cCU5NHZscyU5NHloeVlyJTdCJTk0aXIlN0UlOEUlNjAlODQlOTElN0MlNUR1aWclNjA=|31950540	"
        "3|JTg1JTk0cCU5NnVmJTg0JTk2dWhuJTVCdHolOEQlNjA=|44314626"
    )
    print(get_phones_from_command(cmd))  # ['-00-00', '11-822-14', '-00-00']

    cmd = (
        "1|JTg3JTkyJTdDJTk2dmZxJTk2c2hwWHQlN0IlOEVmdHglOEUlNUIlODQlN0QlN0NXciVBMWElNjA=|23649509	"
        "2|JThBJTk1JTdEJTk0dGtvJTk3cWx3WnJ6bCU5QnV2JTkyJTVFJTg2a3olNUN0bF9k|95446977	"
        "3|JTg1JTkybyU5N3pvJTgzJTkycWhsWnUlN0YlOTZf|40841102"
    )
    print(get_phones_from_command(cmd))  # ['94-711-03', '54-829-39', '-00-00']

    cmd = (
        "1|JTg4V2slOTN1ZnYlOTV1aSU3QiU4RXVWdyU5NXglN0J2JTkycSU3QiU5MiU5OXMlN0QlOTFa|56764591	"
        "2|JThBJTk1dSU4RXlpcCU5NXFsbiU5NHBabiU4Rnh3cCU5NXd2JTk2JTk3bSU3RCU4RCU1Qw==|96021657	"
        "3|JTg4JThGbiU4RnZsJTgzJTkzcWtpWW0lN0IlOTNf|85533937"
    )
    print(get_phones_from_command(cmd))  # ['60-164-75', '51-632-25', '-00-00']

    cmd = (
        "1|JTg3JTdDJTgwVXklOEV6JTVCbyU5RCU3RV9yJUExell0dXpreGclN0RadCU3RSU4RCU5MHglODB1ZQ==|46551687	"
        "2|JTg3ZyU3Q1QlN0MlOEV5JTVFcCU5RCU3Q1clN0RoeSU1RHQlOEQlN0NYJTdEeHlfciU3QiU5RSU4Rnp6bWc=|2094350	"
        "3|JTg0JTk2byU5NnVtJTdDJTkycm5sJTVFcCU3RCU4RSU1Qg==|3088581"
    )
    print(get_phones_from_command(cmd))  # ['49-397-09', '79-935-37', '-00-00']

    cmd = (
        "1|JTg4JTkwayU5M3htJTdFJThGdWtqVnElN0QlOTRa|86770681	"
        "2|JTg5JTk2biU5MnZndiU5NndqJThFJTVCcCU3Q2glQTF0JTdDJTkxXyU4N3klN0NYdyU3QmVj|80583093	"
        "3|JTg3JTkycSU4RXFtJTdCJTk1d2psJTVDbHYlOTRX|74342308"
    )
    print(get_phones_from_command(cmd))  # ['-00-00', '50-328-41', '-00-00']

    cmd = (
        "1|JTg3JThFbyU4RXlpJTdGJThFc2poWmwlN0UlOTAlNUI=|67355029	"
        "2|JTg5cHclOTB2bnMlOTN1aiU4NFduJTdCJTk2aXF6JTkxXyU4NCU4RCU3Q193JTlFY2M=|80050871	"
        "3|JTg4JThFcyU5M3dvJTgwJTk3eWtoJTVFcSU3QyU5NiU1Qw==|84769395"
    )
    print(get_phones_from_command(cmd))  # ['-00-00', '33-212-58', '-00-00']
