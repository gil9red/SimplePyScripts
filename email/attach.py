from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

__author__ = 'ipetrash'

"""Пример отсылки письма, содержащего прикрепленные файлы, "самому себе"."""


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
    msg = MIMEMultipart()
    msg['Subject'] = mail_subject
    msg['From'] = mail_from
    msg['To'] = ', '.join(mail_to)

    msg.attach(MIMEText(mail_text))

    with open('attach_files/im1.png', mode='rb') as f:
        im = MIMEImage(f.read())
        im.add_header('content-disposition', 'attachment', filename='pict')
        msg.attach(im)

    with open('attach_files/im2.jpg', mode='rb') as f:
        im = MIMEImage(f.read())
        im.add_header('content-disposition', 'attachment', filename='im2.jpg')
        msg.attach(im)

    with open('attach_files/hello.html', mode='rb') as f:
        t = MIMEText(f.read(), _charset='utf-8')
        t.add_header('content-disposition', 'attachment', filename='hello.html')
        msg.attach(t)

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