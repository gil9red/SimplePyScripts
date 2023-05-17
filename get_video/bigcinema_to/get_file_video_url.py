#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import re

import requests


# source: https://hms.lostcut.net/viewtopic.php?id=80
def decode_base64_bigcinema_to(base64_data, remove_secret_word=True):
    # Чтобы получить этот словарь заменяемых символов, нужно скачать плеер сайта (формат swf),
    # декодировать его "Flash Decompiler Trillix" и найти списки codec_a и codec_b
    a_to_b_dict = {
        "f": "D",
        "v": "U",
        "=": "E",
        "7": "X",
        "4": "L",
        "W": "H",
        "w": "8",
        "n": "1",
        "e": "M",
        "z": "I",
        "T": "i",
        "Y": "u",
        "m": "o",
        "s": "g",
        "k": "Z",
        "x": "p",
        "J": "N",
        "B": "c",
        "Q": "0",
        "b": "t",
        "a": "R",
        "6": "d",
        "l": "y",
        "5": "3",
        "9": "V",
        "G": "2",
    }

    base64_data = base64_data.replace("\n", "")
    for a, b in a_to_b_dict.items():
        base64_data = base64_data.replace(b, "___")
        base64_data = base64_data.replace(a, b)
        base64_data = base64_data.replace("___", a)

    # secret_words случайно вставляется base64_data, портя его
    # У bigcinema.to секретное слово меняется
    # TODO: Поиграться, и если нужно написать регулярку, которая удалит секретное слово
    # NTgwNA== -> 5804
    # NTkyMQ== -> 5921
    # NzgwOA== -> 7808

    # Секретные слова очень похожие, и можно попытаться регуляркой их заменять
    if remove_secret_word:
        # base64_data = re.sub(r'N.{,5}==', '', base64_data)

        # Или, попытаемся вырезать подстроки, оканчивающиеся на ==
        # Я заметил, что перед == всегда идут 6 символов, и по этому признаку
        # будем удалять такую строку
        # NOTE: или же можно попробовать найти это секретное слово, сделав два запроса,
        # получив 2 base64, а т.к. секретное слово вставляется в случайное место, то нужно
        # просто найти его и удалить
        base64_data = re.sub(r".{,6}==", "", base64_data, count=1)

    data = base64.standard_b64decode(base64_data)
    return data.decode("utf-8")


# Нужно вытащить значение из file
# var flashvals = {
#     uid:            player_id,
#     st:"http://bigcinema.to/templates/framework/swf/default_middle.txt?v=8",
#                     file:"RWaQBfmU4GZYkoNGRGJZtT3jtGQU6 ... JAEEJJ926d0v324GnU6oyyBlwLOf=8JizYt7AQ"
#
# };
GET_FILE_DATA_FROM_FLASHVALS_PATTERN = re.compile(r"""file *?: *?['"](.+?)['"]""")


def get_file_video_url(url):
    rs = requests.get(url)
    if not rs.ok:
        return

    # Значений может быть несколько. И я не разобрался чем отличаются ссылки в file друг от друга,
    # поэтому берем первый попавшийся
    match = GET_FILE_DATA_FROM_FLASHVALS_PATTERN.search(rs.text)
    if match is None:
        return

    return decode_base64_bigcinema_to(match.group(1))


if __name__ == "__main__":
    url = "http://bigcinema.to/movie/menya-zovut-dzhig-robot-lo-chiamavano-jeeg-robot.html"
    print(get_file_video_url(url))

    url = "http://bigcinema.to/movie/pit-i-ego-drakon-petes-dragon.html"
    print(get_file_video_url(url))

    url = "http://bigcinema.to/movie/bokser-marionetka-cardboard-boxer.html"
    print(get_file_video_url(url))
