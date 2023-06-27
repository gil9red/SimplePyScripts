#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Рассмотрим два HTML-документа A и B.
Из A можно перейти в B за один переход, если в A есть ссылка на B, т. е. внутри A есть тег <a href="B">, возможно
с дополнительными параметрами внутри тега.
Из A можно перейти в B за два перехода если существует такой документ C, что из A в C можно перейти за один переход
и из C в B можно перейти за один переход.

Вашей программе на вход подаются две строки, содержащие url двух документов A и B.
Выведите Yes, если из A в B можно перейти за два перехода, иначе выведите No.

Обратите внимание на то, что не все ссылки внутри HTML документа могут вести на существующие HTML документы.

Sample Input 1:
https://stepic.org/media/attachments/lesson/24472/sample0.html
https://stepic.org/media/attachments/lesson/24472/sample2.html

Sample Output 1:
Yes

Sample Input 2:
https://stepic.org/media/attachments/lesson/24472/sample0.html
https://stepic.org/media/attachments/lesson/24472/sample1.html

Sample Output 2:
No

Sample Input 3:
https://stepic.org/media/attachments/lesson/24472/sample1.html
https://stepic.org/media/attachments/lesson/24472/sample2.html

Sample Output 3:
Yes

"""

if __name__ == "__main__":
    import urllib.error
    from urllib.request import urlopen

    from lxml import etree

    url_a = input()
    url_b = input()

    found = False

    try:
        with urlopen(url_a) as f:
            root = etree.HTML(f.read())

            # Перебор ссылок в url_a (первый переход, т.е. A)
            for url_c in root.xpath("//a/@href"):
                try:
                    with urlopen(url_c) as f:
                        if url_b in f.read().decode():
                            found = True
                            break

                except urllib.error.HTTPError:
                    pass

    # Т.е. ошибка произошла только при загрузке и парсинге url_a, что не дает шансов проверить дальше
    # поэтому сразу говорим No
    except (etree.XMLSyntaxError, urllib.error.HTTPError):
        pass

    print("Yes" if found else "No")
