__author__ = 'ipetrash'


# TODO: скачать ранобе "Непутевый ученик в школе магии" и сконвертировать в формат, который
# сможет открыть книгочиталка.
# http://www.baka-tsuki.org/project/index.php?title=Mahouka_Koukou_no_Rettousei_~Russian_Version~
# http://ruranobe.ru/r/mknr
# Первая глава: http://ruranobe.ru/r/mknr/v1#index
# Реализовать скрипт в стиле Unix: программа должна делать только одну функцию и делать ее хорошо,
# т.е. один скрипт скачивает главы, и сохраняет их в html на диске, разделяя их на тома (каждый том,
# отдельная папка), а второй скрипт конвертирует эти главы в формат книгочиталки (например, fb2)

if __name__ == '__main__':
    from grab import Grab
    from urllib.parse import urljoin

    url = 'http://ruranobe.ru/r/mknr'

    g = Grab()
    g.go(url)

    # Получение основного контекста, содержащий аннотацию и ссылки на тома
    content_text = g.doc.select('//div[@id="mw-content-text"]')

    # Получение названия ранобе
    name = g.doc.select('//h1[@id="firstHeading"]').text()

    # Получение и объединение параграфов в единый текст
    annotation = '\n'.join(r.text() for r in content_text.select('p/i'))

    # Получение списка томов
    list_volume = content_text.select('ul/li/a')

    print("Название: '{}'".format(name))
    print("\nАннотации:\n'{}'".format(annotation))
    print("\nТома ({}):".format(len(list_volume)))
    for n, volume in enumerate(list_volume, 1):
        # Соединение адреса к главной странице ранобе и относительной ссылки к тому
        url_volume = urljoin(url, volume.attr('href'))

        # Переходим на страницу тома
        g.go(url_volume)

        # Относительная ссылка к обложки тома
        relative_url_cover = g.doc.select('//td[@id="cover"]/a').attr('href')

        # Соединение адреса к главной странице ранобе и относительной ссылки к обложки тома
        url_cover_volume = urljoin(url, relative_url_cover)

        print("{}. '{}'\n    {}\n    {}".format(n, volume.text(),
                                                url_volume,
                                                url_cover_volume))

        # Получаем список строк с двумя столбцами, каждая строка содержит
        # некоторую информацию о томе: названия на нескольких языка, серия,
        # автор, иллюстратор и т.п.
        list_info = g.doc.select('//table[@id="release-info"]/tr')
        volume_name = list_info[2].select('td')[1].text()
        series = list_info[3].select('td')[1].text()
        author = list_info[4].select('td')[1].text()
        illustrator = list_info[5].select('td')[1].text()
        volume_isbn = list_info[6].select('td')[1].text()

        print("    Название:    {}".format(volume_name))
        print("    Серия:       {}".format(series))
        print("    Автор:       {}".format(author))
        print("    Иллюстратор: {}".format(illustrator))
        print("    ISBN:        {}".format(volume_isbn))

        # for info in list_info:
        #     # Получение списка столбцов
        #     td = info.select('td')
        #     print("    {}: '{}'".format(td[0].text(), td[1].text()))

        print()