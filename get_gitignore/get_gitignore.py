__author__ = 'ipetrash'


"""Скрипт возвращает содержимое gitignore для языков программирования"""


if __name__ == '__main__':
    from grab import Grab
    g = Grab()

    lang = input("Input: ")
    g.go("https://www.gitignore.io/api/" + lang)
    print(g.response.body)