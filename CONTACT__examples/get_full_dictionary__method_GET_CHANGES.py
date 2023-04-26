#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт выполняет запрос получения справочника CONTACT (метод GET_CHANGES).

"""


from config import *

import requests


FILE_NAME_FULL_DICT = "full_dict__CONTACT.xml"


if __name__ == "__main__":
    post_data = """
    <?xml version="1.0"?>
    <REQUEST OBJECT_CLASS="TAbonentObject" ACTION="GET_CHANGES" VERSION="0" TYPE_VERSION="I" PACK="ZLIB"
    INT_SOFT_ID="{INT_SOFT_ID}"
    POINT_CODE="{POINT_CODE}"
    SignOut="No"
    ExpectSigned="No"
    />
    """.format(
        INT_SOFT_ID=INT_SOFT_ID, POINT_CODE=POINT_CODE
    )

    rs = requests.post(URL_NG_SERVER, data=post_data)
    print(rs)
    print(len(rs.text))

    with open(FILE_NAME_FULL_DICT, "wb") as f:
        f.write(rs.content)

    print("Write to: {}".format(FILE_NAME_FULL_DICT))
