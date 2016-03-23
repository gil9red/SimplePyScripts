#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urlsplit
import base64


def get_today_RFC1123_date():
    from datetime import datetime
    from babel.dates import format_datetime

    now = datetime.utcnow()
    format = 'EEE, dd LLL yyyy hh:mm:ss'
    return format_datetime(now, format, locale='en') + ' GMT'


def hmac_sha256(key, msg):
    import hmac
    import hashlib
    signature = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def get_authorization_header(application_id, secret, today_date, url):
    secret = base64.b64decode(secret)

    message = "GET\n\n{}\n{}".format(today_date, urlsplit(url).path).encode()
    signature = hmac_sha256(secret, message)

    return "UNIHMAC {}:{}".format(application_id, signature)


SECRET = '<SECRET>'
APPLICATION_ID = '<APPLICATION_ID>'

URL = 'https://test.api.unistream.com/v1/agents'
TODAY_DATE = get_today_RFC1123_date()

headers = {
    'Authorization': get_authorization_header(APPLICATION_ID,
                                              SECRET,
                                              TODAY_DATE,
                                              URL),
    'Date': TODAY_DATE,
}

import requests
rs = requests.get(URL, headers=headers)
print(rs)
print(rs.text)
