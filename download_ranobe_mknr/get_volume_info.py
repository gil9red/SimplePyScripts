__author__ = 'ipetrash'


"""Модуль для возвращения информации о томе ранобе."""


from grab import Grab
from urllib.parse import urljoin


def volume_info(url_volume, url_ranobe):
    """Функция возвращает словарь, содержащий информацию о томе ранобе."""

    g = Grab()
    g.setup(hammer_mode=True)

    # Переходим на страницу тома
    g.go(url_volume)

    if g.response.code != 200:
        # TODO: кажется, лучше выкидывать исключения с описанием причины
        print("Страница: {}, код возврата: {}".format(url_volume, g.response.code))
        return

    # Получение списка глав из оглавления
    contents = g.doc.select('//div[@id="index"]/*/li/a')
    # Если нет содержания -- пропускаем том
    if not contents:
        # TODO: кажется, лучше выкидывать исключения с описанием причины
        print("Нет содержания: {}".format(url_volume))
        return

    # Относительная ссылка к обложки тома
    relative_url_cover = g.doc.select('//td[@id="cover"]/a').attr('href')

    # Соединение адреса к главной странице ранобе и относительной ссылки к обложке тома
    url_cover_volume = urljoin(url_ranobe, relative_url_cover)

    # Получаем список строк с двумя столбцами, каждая строка содержит
    # некоторую информацию о томе: названия на нескольких языка, серия,
    # автор, иллюстратор и т.п.
    list_info = g.doc.select('//table[@id="release-info"]/tr/td[2]')
    volume_name = list_info[2].text()
    series = list_info[3].text()
    author = list_info[4].text()
    illustrator = list_info[5].text()
    volume_isbn = list_info[6].text()

    # Список глав тома
    chapters = list()
    for ch in contents:
        # Адрес к главе тома
        url_chapter = urljoin(url_ranobe, ch.attr("href"))

        # Проверка на существование страницы с главой
        grab_chapter = Grab()
        grab_chapter.setup(hammer_mode=True)
        grab_chapter.go(url_chapter)

        # Если не удачно, выходим
        if grab_chapter.response.code != 200:
            # TODO: кажется, лучше выкидывать исключения с описанием причины
            # TODO: фильтровать типы глав по нужности
            print("Не найдена глава: {}".format(url_chapter))
            return

        # Добавление адреса главы к списку
        chapters.append(url_chapter)

    info = {
        "name": volume_name,
        "series": series,
        "author": author,
        "illustrator": illustrator,
        "ISBN": volume_isbn,
        "url_cover": url_cover_volume,
        "chapters": chapters,
    }
    return info