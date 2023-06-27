#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вашей программе на вход подается ссылка на HTML файл.
Вам необходимо скачать этот файл, затем найти в нем все ссылки вида <a ... href="..." ... > и вывести список сайтов,
на которые есть ссылка.

Сайтом в данной задаче будем называть имя домена вместе с именами поддоменов. То есть, это последовательность символов,
которая следует сразу после символов протокола, если он есть, до символов порта или пути, если они есть, за исключением
случаев с относительными ссылками вида
<a href="../some_path/index.html">﻿.

Сайты следует выводить в алфавитном порядке.

Пример HTML файла:
<a href="http://stepic.org/courses">
<a href='https://stepic.org'>
<a href='http://neerc.ifmo.ru:1345'>
<a href="ftp://mail.ru/distib" >
<a href="ya.ru">
<a href="www.ya.ru">
<a href="../skip_relative_links">

Пример ответа:
mail.ru
neerc.ifmo.ru
stepic.org
www.ya.ru
ya.ru

"""


if __name__ == "__main__":
    import re
    from urllib.request import urlopen, urlparse

    # Скачивание страницы, декодирование из байтов в строку
    text = urlopen(input()).read().decode()

    urls = set()

    # Поиск ссылок в тексте
    for url in re.findall(r"""<a.+href=["'](.+?)['"].*>""", text, flags=re.MULTILINE):
        # Разбор строки url на компоненты
        result = urlparse(url)
        result = result.path if not result.netloc else result.netloc

        # Избавляемся от порта
        if ":" in result:
            result = result.split(":")[0]

        # Избавляемся от относительных ссылок
        if result.startswith("../"):
            continue

        urls.add(result)

    for url in sorted(urls):
        print(url)
