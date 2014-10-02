__author__ = 'ipetrash'


"""Скрипт, используя сервис http://sms.ru, отправляет смс."""


if __name__ == '__main__':
    # Статья: http://habrahabr.ru/post/211667/
    # API: http://sms.ru/?panel=api&subpanel=method&show=sms/send

    import urllib.request

    api_id = "435fd045-bbf1-aa14-fd75-4e965b077490"
    to = "79123267932"
    mess = "Хадсону стало плохо! =("
    mess = urllib.request.quote(mess)
    url = "http://sms.ru/sms/send?api_id={}&to={}&text={}"
    url = url.format(api_id, to, mess)

    # urllib.request.urlopen(url)
    from grab import Grab
    g = Grab()
    g.go(url)

    # Значения кода указано в http://sms.ru/?panel=api&subpanel=method&show=sms/send
    print("code: {}".format(g.response.body))