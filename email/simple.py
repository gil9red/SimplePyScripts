import smtplib
from email.mime.text import MIMEText

__author__ = 'ipetrash'

"""Пример отсылки письма "самому себе"."""


# http://www.tutorialspoint.com/python/python_sending_email.htm
# https://docs.python.org/3.4/library/email-examples.html

if __name__ == '__main__':
    mail_sender = 'USERNAME@DOMAIN'
    mail_passwd = 'PASSWORD'

    smtp_server = 'YOUR.MAIL.SERVER'
    port = 587

    mail_text = 'Example!\nFirst!\nSecond!\n\nРаз!\nДва!\nТри!'
    mail_subject = 'Здарова чувак! Hello!!!'
    mail_from = mail_sender
    mail_to = [mail_sender]
    # Несколько получателей указываются через запятую:
    # mail_to = [mail_sender, '*****@mail.com']

    # Create a text/plain message
    msg = MIMEText(mail_text)
    msg['Subject'] = mail_subject
    msg['From'] = mail_from
    msg['To'] = ', '.join(mail_to)

    try:
        # Send the message on SMTP server.
        s = smtplib.SMTP(smtp_server, port)
        s.starttls()
        s.login(mail_sender, mail_passwd)

        try:
            s.send_message(msg)
        finally:
            s.quit()

        print('Email sent')

    except Exception as e:
        print('Error sending mail: ' + str(e))