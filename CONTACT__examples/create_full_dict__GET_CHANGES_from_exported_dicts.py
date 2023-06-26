#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Функция из отдельный файлов справки в формате XML собирает в одном файле,
идентичном ответу от запроса GET_CHANGES.

"""

import base64
import glob
import os
import zlib


def bytes_to_compress_to_base64(bytes_text: bytes) -> str:
    """
    Функция сжимает байтовый массив и кодирует его как base64 и возвращает как строку.

    """

    compress_bytes_xml = zlib.compress(bytes_text)
    base64_compress = base64.b64encode(compress_bytes_xml)
    return base64_compress.decode("utf-8")


if __name__ == "__main__":
    DIR_DICT_CONTACT = "mini_full_dict__CONTACT"
    FILE_NAME_FULL_DICT = "new_mini_full_dict__CONTACT.xml"

    HTML_PATTERN_RESPONSE__GET_CHANGES = """\
<RESPONSE SIGN_IT="0" VERSION="15" FULL="1" RE="0" ERR_TEXT="" NOLOG="1"
GLOBAL_VERSION="15.11.2013 12:37:40" GLOBAL_VERSION_SERVER="23.01.2014 16:33:23">{}</RESPONSE>
    """

    child_list = list()

    for file_name in glob.glob(DIR_DICT_CONTACT + "/*.xml"):
        print(file_name)

        dict_name = os.path.splitext(os.path.basename(file_name))[0].upper()

        bytes_xml = open(file_name, "rb").read()
        base64_str = bytes_to_compress_to_base64(bytes_xml)

        child_list.append(f"<{dict_name}>{base64_str}</{dict_name}>")

    with open(FILE_NAME_FULL_DICT, "w", encoding="utf-8") as f:
        f.write(HTML_PATTERN_RESPONSE__GET_CHANGES.format("".join(child_list)))

    print()
    print(f"Write to {FILE_NAME_FULL_DICT}")
