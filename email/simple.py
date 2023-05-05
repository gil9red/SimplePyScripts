#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


"""Пример отсылки простого письма самому себе."""


# http://www.tutorialspoint.com/python/python_sending_email.htm
# https://docs.python.org/3.4/library/email-examples.html


import sys

# this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP_SSL as SMTP

from email.mime.text import MIMEText


SMTPserver = "smtp.att.yahoo.com"
sender = "me@my_email_domain.net"
destination = ["recipient@her_email_domain.com"]

USERNAME = "USER_NAME_FOR_INTERNET_SERVICE_PROVIDER"
PASSWORD = "PASSWORD_INTERNET_SERVICE_PROVIDER"

# typical values for text_subtype are plain, html, xml
text_subtype = "plain"


content = """\
Test message
"""

subject = "Sent from Python"

try:
    msg = MIMEText(content, text_subtype)
    msg["Subject"] = subject
    msg["From"] = sender  # some SMTP servers will do this automatically, not all

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.close()

except Exception as e:
    sys.exit("mail failed; %s" % str(e))  # give a error message
