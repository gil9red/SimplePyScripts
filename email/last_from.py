#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import email
import imaplib
import sys
import logging

from datetime import date, timedelta


logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s",
)

username = "<username>"
password = "<password>"
smtp_server = "<smtp_server>"
from_email = "<from_email>"


def get_last_lunch_menu():
    """
    Функция возвращает последнее письмо от указанного емейла.

    """

    logging.debug("Check last email.")

    connect = imaplib.IMAP4(smtp_server)
    connect.login(username, password)
    connect.select()

    # Если не ограничивать датой, соберет все письма и запрос будет дольше выполняться
    today = date.today()
    week_ago = today - timedelta(weeks=1)
    since = week_ago.strftime("%d-%b-%Y")

    logging.debug("Search emails from %s.", from_email)
    typ, msgnums = connect.search(None, "HEADER From", from_email, "SINCE", since)
    logging.debug("Search result: %s.", msgnums[0].split())

    last_id = msgnums[0].split()[-1]
    typ, data = connect.fetch(last_id, "(RFC822)")

    msg = email.message_from_bytes(data[0][1])

    connect.close()
    connect.logout()

    return msg


if __name__ == "__main__":
    msg = get_last_lunch_menu()
    print(msg)
