__author__ = "ipetrash"


"""Пример отсылки письма, содержащего обычный текст и html, "самому себе"."""


import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# http://www.tutorialspoint.com/python/python_sending_email.htm
# https://docs.python.org/3.4/library/email-examples.html

if __name__ == "__main__":
    mail_sender = "USERNAME@DOMAIN"  # Например: vasyapupkin@mail.ru
    mail_passwd = "PASSWORD"  # Пароль к почте

    smtp_server = "YOUR.MAIL.SERVER"  # Например: smtp.mail.ru
    port = 587

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

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = """
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="https://www.python.org">link</a> you wanted.
        </p>
      </body>
    </html>
    """

    msg.attach(MIMEText(text))
    msg.attach(MIMEText(html, _subtype="html"))
    msg.attach(MIMEText(html))

    try:
        # Send the message on SMTP server.
        with smtplib.SMTP(smtp_server, port) as s:
            s.starttls()
            s.login(mail_sender, mail_passwd)
            s.send_message(msg)

            print("Email sent")

    except Exception as e:
        print("Error sending mail: " + str(e))
