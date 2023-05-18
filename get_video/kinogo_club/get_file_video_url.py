#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import re

import requests


# Алгоритм: https://hms.lostcut.net/viewtopic.php?id=80


def decode_uppod_tr(data, ch1, ch2):
    if data[:-1].endswith(ch1) and data[2] == ch2:
        srev = data[::-1]  # revers string
        try:
            loc3 = int(float(srev[-2:]) / 2)  # get number at end of string
        except ValueError:
            return data
        srev = srev[2:-3]  # get string between ch1 and ch2
        if loc3 < len(srev):
            i = loc3
            while i < len(srev):
                srev = srev[:i] + srev[i + 1 :]  # remove char at index i
                i += loc3
        data = srev + "!"
    return data


def decode_uppod_text_hash(data):
    hash = "0123456789WGXMHRUZID=NQVBLihbzaclmepsJxdftioYkngryTwuvihv7ec41D6GpBtXx3QJRiN5WwMf=ihngU08IuldVHosTmZz9kYL2bayE"
    data = decode_uppod_tr(data, "r", "A")
    data = data.replace("\n", "")
    hash = hash.split("ih")

    if data.endswith("!"):
        data = data[:-1]
        taba = hash[3]
        tabb = hash[2]
    else:
        taba = hash[1]
        tabb = hash[0]

    i = 0
    while i < len(taba):
        data = data.replace(tabb[i], "__")
        data = data.replace(taba[i], tabb[i])
        data = data.replace("__", taba[i])
        i += 1

    result = base64.b64decode(data)
    return result


def decode_file_url(base64_data):
    # secret_word случайно вставляется base64_data, портя его
    secret_word = "tQ3N"
    file_url = decode_uppod_text_hash(base64_data.replace(secret_word, ""))
    return file_url.decode("utf-8")


# Вытаскивание закодированного в base64 html кода, описывающего плеер
base64_uppod_data_pattern = re.compile(r"document\.write\(Base64.decode\('(.+?)'\)")

# Вытаскивание закодированного в измененный base64 ссылки на файл видео
base64_data_url_pattern = re.compile(r"&amp;file=(.+?)&amp;")


def get_file_video_url(url):
    rs = requests.get(url)
    if not rs.ok:
        return

    match = base64_uppod_data_pattern.search(rs.text)
    if match is None:
        return

    uppod_data_base64 = match.group(1)
    uppod_data = base64.standard_b64decode(uppod_data_base64).decode("utf-8")
    match = base64_data_url_pattern.search(uppod_data)
    if match is None:
        return

    return decode_file_url(match.group(1))


if __name__ == "__main__":
    url = "http://kinogo.club/6246-pervyy-mstitel-3-protivostoyanie-2016.html"
    print(get_file_video_url(url))

    url = "http://kinogo.club/6253-sudnaya-noch-3-2016.html"
    print(get_file_video_url(url))

    url = "http://kinogo.club/2963-poceluy-mamochku-na-noch-2013.html"
    print(get_file_video_url(url))
