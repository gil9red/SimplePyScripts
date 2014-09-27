__author__ = 'ipetrash'


"""
Пример того как можно узнать свой ip,
используя запрос на сайт и модуль grab.
"""


from grab import Grab


if __name__ == '__main__':
    g = Grab()
    g.go("http://api.wipmania.com")
    context = g.response.body
    data = context.split("<br>")
    ip = data[0]
    print("My IP: {}".format(ip))