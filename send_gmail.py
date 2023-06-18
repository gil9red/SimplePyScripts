#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from email.mime.text import MIMEText

# This invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP_SSL as SMTP
#
# Use this for standard SMTP protocol (port 25, no encryption)
# from smtplib import SMTP


# Указывает нужно ли выводить сообщения общения smtp сервера и
# нашего скрипта при отправке писем
debug_smtp = True
debug_smtp = False

username = "<username>"
password = "<password>"

smtp_server = "smtp.gmail.com"

# email отправителя, т.е. наша почта
sender = username

# email, на которое нужно отправить письма с заказом меню
to_email = "<to_email>"

# Получатели копии письма
to_cc_emails = [
    # sender,
]

subject = "Pyhton test"
text = "Pyhton test\Pyhton test\Pyhton test\Pyhton test"


# typical values for text_subtype are plain, html, xml
text_subtype = "plain"

msg = MIMEText(text, text_subtype)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = to_email
msg["Cc"] = ", ".join(to_cc_emails)

with SMTP(smtp_server, 465) as smtp:
    smtp.set_debuglevel(debug_smtp)
    smtp.login(username, password)
    smtp.send_message(msg)
