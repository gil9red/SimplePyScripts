__author__ = 'ipetrash'


# TODO: скачать ранобе "Непутевый ученик в школе магии" и сконвертировать в формат, который
# сможет открыть книгочиталка.
# http://www.baka-tsuki.org/project/index.php?title=Mahouka_Koukou_no_Rettousei_~Russian_Version~
# http://ruranobe.ru/r/mknr
# Первая глава: http://ruranobe.ru/r/mknr/v1#index
# Реализовать скрипт в стиле Unix: программа должна делать только одну функцию и делать ее хорошо,
# т.е. один скрипт скачивает главы, и сохраняет их в html на диске, разделяя их на тома (каждый том,
# отдельная папка), а второй скрипт конвертирует эти главы в формат книгочиталки (например, fb2)

# from grab import Grab
# from urllib.parse import urljoin
# from os import makedirs
# import os.path


import get_ranobe_info
import get_volume_info
from urllib.parse import urljoin


if __name__ == '__main__':
    ranobe = get_ranobe_info.ranobe_info()

    url = ranobe["url"]
    name_ranobe = ranobe["name"]
    annotation = ranobe["annotation"]
    list_volumes = ranobe["list_volumes"]

    # # В папке с скриптом создаем папку c названием name_ranobe
    # if not os.path.exists(name_ranobe):
    #     makedirs(name_ranobe)

    print("Название: '{}'".format(name_ranobe))
    print("\nАннотации:\n'{}'".format(annotation))
    print("\nТома ({}):".format(len(list_volumes)))

    for n, v in enumerate(list_volumes, 1):
        print("Глава {}:".format(n))

        # Соединение адреса к главной странице ранобе и относительной ссылки к тому
        url_volume = urljoin(url, v.attr('href'))

        volume_info = get_volume_info.volume_info(url_volume, url)
        if volume_info:
            print("  Адрес тома: {}".format(url_volume))
            print("  ALL: {}".format(volume_info))
            print("    Название:    {}".format(volume_info.get("name")))
            print("    Серия:       {}".format(volume_info.get("series")))
            print("    Автор:       {}".format(volume_info.get("author")))
            print("    Иллюстратор: {}".format(volume_info.get("illustrator")))
            print("    ISBN:        {}".format(volume_info.get("ISBN")))
            print("    Обложка:     {}".format(volume_info.get("url_cover")))
            print("    Содержание:")
            print("        Начальные иллюстрации: {}".format(volume_info.get("i")))
            print("        Вступление: {}".format(volume_info.get("p1")))
            print("        Пролог: {}".format(volume_info.get("p2")))
            print("        Главы:")
            for i, ch in enumerate(volume_info.get("chapters"), 1):
                print("            {}. '{}'".format(i, ch))
            print("        Эпилог: {}".format(volume_info.get("e")))
            print("        Послесловие: {}".format(volume_info.get("a")))
            print("        Запоздавший шедевр: {}".format(volume_info.get("a2")))
        else:
            print("Неудача с томом: {}".format(url_volume))

        print()