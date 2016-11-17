#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# source: https://hms.lostcut.net/viewtopic.php?id=80
def decode_base64_bigcinema_to(base64_data):
    # Чтобы получить этот словарь заменяемых символов, нужно скачать плеер сайта (формат swf),
    # декодировать его "Flash Decompiler Trillix" и найти списки codec_a и codec_b
    a_to_b_dict = {'f': 'D', 'v': 'U', '=': 'E', '7': 'X', '4': 'L', 'W': 'H', 'w': '8', 'n': '1', 'e': 'M', 'z': 'I',
                   'T': 'i', 'Y': 'u', 'm': 'o', 's': 'g', 'k': 'Z', 'x': 'p', 'J': 'N', 'B': 'c', 'Q': '0', 'b': 't',
                   'a': 'R', '6': 'd', 'l': 'y', '5': '3', '9': 'V', 'G': '2'}

    base64_data = base64_data.replace('\n', '')
    for a, b in a_to_b_dict.items():
        base64_data = base64_data.replace(b, '___')
        base64_data = base64_data.replace(a, b)
        base64_data = base64_data.replace('___', a)

    # secret_word случайно вставляется base64_data, портя его
    secret_word = 'NTkyMQ=='
    base64_data = base64_data.replace(secret_word, '')

    import base64
    data = base64.standard_b64decode(base64_data)
    return data.decode('utf-8')


print(decode_base64_bigcinema_to('RWaQBfmU4GZYkoNGRGJZtT3jtGQU62yQt2vUv5NTeQy3Bo3yaFNISyslafAltIFrM76LiZajJv3v07hORogp0JiZle0EEv324GnU6oyyBlwLOf=8JizYt7AQ'))
print(decode_base64_bigcinema_to('RWaQBfmU4GZYkoNGRGJZtT3jtGQU62yQtJiZle0EE2vUM7kKHo9=Blnb0ikSvfkOknz8RWubR76LiZajJv3v0icJMZQI0v324GnU6oyyBlw5Jiu5OiZYt7AQ'))
print(decode_base64_bigcinema_to('RWaQBfmU4GZYkoNGRGJZtT3jtGQU62yQt2vU0iNdS5yHOWJHkWk2RFNz6Q9R0IcYM76LiZajJv3v0icPa==I0v324GnU6oyyBlwpefJiZle0EEA5Jizp4on8JAEE'))
