__author__ = 'ipetrash'

## Пример того как можно узнать свой ip, используя запрос на сайт.

import urllib.request

if __name__ == '__main__':
    with urllib.request.urlopen("http://api.wipmania.com") as f:
       context = f.read().decode()
       data = context.split("<br>")
       ip = data[0]
       print("My IP: {}".format(ip))