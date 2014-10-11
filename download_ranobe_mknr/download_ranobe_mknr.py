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

    for v in list_volumes:
        # Соединение адреса к главной странице ранобе и относительной ссылки к тому
        url_volume = urljoin(url, v.attr('href'))

        volume_info = get_volume_info.volume_info(url_volume, url)
        if volume_info:
            print("{}: {}".format(volume_info["name"], volume_info))
        else:
            print(url_volume)

        # g = Grab()
        #
        # # Переходим на страницу тома
        # g.go(url_volume)
        #
        # if g.response.code != 200:
        #     print("Страница: {}, код возврата: {}".format(url_volume, g.response.code))
        #     continue
        #
        # # Получение списка глав из оглавления
        # # TODO: если нет содержания -- пропускать том
        # contents = g.doc.select('//div[@id="index"]/*/li/a')
        # if not contents:
        #     print("Нет содержания: {}".format(url_volume))
        #     continue
        #
        # # Относительная ссылка к обложки тома
        # relative_url_cover = g.doc.select('//td[@id="cover"]/a').attr('href')
        #
        # # Соединение адреса к главной странице ранобе и относительной ссылки к обложке тома
        # url_cover_volume = urljoin(url, relative_url_cover)
        #
        # print("{}. '{}'\n    {}\n    {}".format(n, volume.text(),
        #                                         url_volume,
        #                                         url_cover_volume))
        #
        # # Получаем список строк с двумя столбцами, каждая строка содержит
        # # некоторую информацию о томе: названия на нескольких языка, серия,
        # # автор, иллюстратор и т.п.
        # list_info = g.doc.select('//table[@id="release-info"]/tr/td[2]')
        # volume_name = list_info[2].text()
        # series = list_info[3].text()
        # author = list_info[4].text()
        # illustrator = list_info[5].text()
        # volume_ISBN = list_info[6].text()
        #
        # # # Создаем в папке ранобе папку с названием тома
        # # path_dir_volume = os.path.join(name_ranobe, volume_name)
        # # path_dir_volume = path_dir_volume.replace(':', '.')
        # # if not os.path.exists(path_dir_volume):
        # #     makedirs(path_dir_volume)
        #
        # print("    Название:    {}".format(volume_name))
        # print("    Серия:       {}".format(series))
        # print("    Автор:       {}".format(author))
        # print("    Иллюстратор: {}".format(illustrator))
        # print("    ISBN:        {}".format(volume_ISBN))
        #
        # print("    Содержание:")
        # for i, ch in enumerate(contents, 1):
        #     # Адрес к главе тома
        #     url_chapter = urljoin(url, ch.attr("href"))
        #
        #     # Проверка на существование страницы с главой
        #     grab_chapter = Grab()
        #     grab_chapter.go(url_chapter)
        #     if grab_chapter.response.code == 200:
        #         print("        {}. '{}': {}".format(i, ch.text(), url_chapter))
        #     else:
        #         print("Нет главы: {}".format(url_chapter))
        #
        # print()