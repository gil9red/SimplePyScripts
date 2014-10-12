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
            print("    Название:    {}".format(volume_info["name"]))
            print("    Серия:       {}".format(volume_info["series"]))
            print("    Автор:       {}".format(volume_info["author"]))
            print("    Иллюстратор: {}".format(volume_info["illustrator"]))
            print("    ISBN:        {}".format(volume_info["ISBN"]))
            print("    Содержание:")
            for i, ch in enumerate(volume_info["chapters"], 1):
                print("        {}. '{}'".format(i, ch))
        else:
            print("Неудача с томом: {}".format(url_volume))

        print()