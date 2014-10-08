__author__ = 'ipetrash'


"""Скрипт возвращает список доменных зон"""


if __name__ == '__main__':
    from grab import Grab
    g = Grab()
    g.go('http://snowgate.info/zones_list_dns.html')
    print(', '.join(d.text() for d in g.doc.select('//td/strong')))