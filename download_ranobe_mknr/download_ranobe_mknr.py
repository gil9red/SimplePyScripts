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
        # Относительная ссылка на том
        href = volume.attr('href')

        # Соединение адреса к главной странице ранобе и относительной ссылки к тому
        url_volume = urljoin(url, href)

        print("{}. '{}' {}".format(n, volume.text(), url_volume))