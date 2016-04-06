#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


"""Пример отсылки простого письма самому себе."""


import smtplib
from email.mime.text import MIMEText


# http://www.tutorialspoint.com/python/python_sending_email.htm
# https://docs.python.org/3.4/library/email-examples.html

# if __name__ == '__main__':
#     mail_sender = 'USERNAME@DOMAIN'  # Например: vasyapupkin@mail.ru
#     mail_passwd = 'PASSWORD'  # Пароль к почте
#
#     smtp_server = 'YOUR.MAIL.SERVER'  # Например: smtp.mail.ru
#     port = 587
#
#     mail_text = 'Example!\nFirst!\nSecond!\n\nРаз!\nДва!\nТри!'
#     mail_subject = 'Здарова чувак! Hello!!!'
#     mail_from = mail_sender
#     mail_to = [
#         mail_sender
#         # , '*****@mail.com',
#         # ...
#     ]
#     # mail_cc = [
#     # # '*****@mail.com',
#     #     # '*****@gmail.com',
#     # ...
#     # ]
#
#     # Create a text/plain message
#     msg = MIMEText(mail_text)
#     msg['From'] = mail_from
#     msg['To'] = ', '.join(mail_to)
#     # msg['Cc'] = ', '.join(mail_cc)  # Получатели копии письма
#     msg['Subject'] = mail_subject
#
#     try:
#         # Send the message on SMTP server.
#         with smtplib.SMTP(smtp_server, port) as s:
#             s.starttls()
#             s.login(mail_sender, mail_passwd)
#             s.send_message(msg)
#
#             print('Email sent')
#
#     except Exception as e:
#         print('Error sending mail: ' + str(e))


# import smtplib
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
#
# msg = MIMEMultipart()
# msg['From'] = 'me@gmail.com'
# msg['To'] = 'you@gmail.com'
# msg['Subject'] = 'simple email in python'
# message = 'here is the email'
# msg.attach(MIMEText(message))
#
# mailserver = smtplib.SMTP('smtp.gmail.com',587)
# # identify ourselves to smtp gmail client
# mailserver.ehlo()
# # secure our email with tls encryption
# mailserver.starttls()
# # re-identify ourselves as an encrypted connection
# mailserver.ehlo()
# mailserver.login('me@gmail.com', 'mypassword')
#
# mailserver.sendmail('me@gmail.com','you@gmail.com',msg.as_string())
#
# mailserver.quit()


SMTPserver = 'smtp.att.yahoo.com'
sender =     'me@my_email_domain.net'
destination = ['recipient@her_email_domain.com']

USERNAME = "USER_NAME_FOR_INTERNET_SERVICE_PROVIDER"
PASSWORD = "PASSWORD_INTERNET_SERVICE_PROVIDER"

# typical values for text_subtype are plain, html, xml
text_subtype = 'plain'


content="""\
Test message
"""

subject="Sent from Python"

import sys

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
from email.mime.text import MIMEText

try:
    msg = MIMEText(content, text_subtype)
    msg['Subject']=       subject
    msg['From']   = sender # some SMTP servers will do this automatically, not all

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.close()

except Exception as e:
    sys.exit( "mail failed; %s" % str(e) ) # give a error message
