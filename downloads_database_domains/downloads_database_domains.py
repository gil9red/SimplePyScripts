__author__ = 'ipetrash'


"""Скрипт скачивает базу доменов в зоне ru и выводит ее в лог"""


if __name__ == '__main__':
    from urllib.request import urlretrieve
    from os.path import basename
    url = 'https://partner.r01.ru/zones/ru_domains.gz'
    file_name = basename(url)

    # Скачиваем архив
    urlretrieve(url, file_name)

    import gzip

    # Открытие архива
    with gzip.open(file_name, 'rb') as f:
        c = 1
        # Построчный вывод архивированного файла
        for line in f:
            print("{} {}".format(c, line))
            c += 1