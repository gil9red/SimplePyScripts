from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

__author__ = "ipetrash"

"""Пример отсылки письма, содержащего прикрепленные файлы, "самому себе"."""


# http://www.tutorialspoint.com/python/python_sending_email.htm
# https://docs.python.org/3.4/library/email-examples.html

if __name__ == "__main__":
    mail_sender = "USERNAME@DOMAIN"  # Например: vasyapupkin@mail.ru
    mail_passwd = "PASSWORD"  # Пароль к почте

    smtp_server = "YOUR.MAIL.SERVER"  # Например: smtp.mail.ru
    port = 587

    mail_text = "Example!\nFirst!\nSecond!\n\nРаз!\nДва!\nТри!"
    mail_subject = "Здарова чувак! Hello!!!"
    mail_from = mail_sender
    mail_to = [
        mail_sender
        # , '*****@mail.com',
        # ...
    ]
    # mail_cc = [
    # # '*****@mail.com',
    #     # '*****@gmail.com',
    # ...
    # ]

    # Create a text/plain message
    msg = MIMEMultipart()
    msg["From"] = mail_from
    msg["To"] = ", ".join(mail_to)
    # msg['Cc'] = ', '.join(mail_cc)  # Получатели копии письма
    msg["Subject"] = mail_subject

    msg.attach(MIMEText(mail_text))

    with open("attach_files/im1.png", mode="rb") as f:
        im = MIMEImage(f.read())
        im.add_header("content-disposition", "attachment", filename="pict")
        msg.attach(im)

    with open("attach_files/im2.jpg", mode="rb") as f:
        im = MIMEImage(f.read())
        im.add_header("content-disposition", "attachment", filename="im2.jpg")
        msg.attach(im)

    with open("attach_files/hello.html", mode="rb") as f:
        t = MIMEText(f.read(), _charset="utf-8")
        t.add_header("content-disposition", "attachment", filename="hello.html")
        msg.attach(t)

    try:
        # Send the message on SMTP server.
        with smtplib.SMTP(smtp_server, port) as s:
            s.starttls()
            s.login(mail_sender, mail_passwd)
            s.send_message(msg)

            print("Email sent")

    except Exception as e:
        print("Error sending mail: " + str(e))
