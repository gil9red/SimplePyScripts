#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://ru.wikipedia.org/wiki/Криптосистема_с_открытым_ключом


# Разбор примера шифрования с помощью справочника: https://ru.wikipedia.org/wiki/Криптосистема_с_открытым_ключом
REFERENCE_GUIDE_NAME_NUM = {
    "Королёв": "5643452",
    "Орехов": "3572651",
    "Рузаева": "4673956",
    "Осипов": "3517289",
    "Батурин": "7755628",
    "Кирсанова": "1235267",
    "Арсеньева": "8492746",
}

# Обратный словарь -- ключом будет число, а значением имя
REFERENCE_GUIDE_NUM_NAME = {v: k for k, v in REFERENCE_GUIDE_NAME_NUM.items()}

MESS = "коробка"


def encrypt(mess):
    keys = REFERENCE_GUIDE_NAME_NUM.keys()
    crypto_text_list = list()

    for c in mess.lower():
        encrypt_key = sorted(filter(lambda x: x[0].lower() == c, keys))[0]
        crypto_text_list.append(REFERENCE_GUIDE_NAME_NUM[encrypt_key])

    return "@".join(crypto_text_list)


def decrypt(encrypt_mess):
    crypto_num_list = encrypt_mess.split("@")
    mess = ""

    for num in crypto_num_list:
        mess += REFERENCE_GUIDE_NUM_NAME[num][0].lower()

    return mess


encrypt_mess = encrypt(MESS)

print(f"Encrypt: {MESS} -> {encrypt_mess}.")
print(f"Decrypt: {encrypt_mess} -> {decrypt(encrypt_mess)}")
