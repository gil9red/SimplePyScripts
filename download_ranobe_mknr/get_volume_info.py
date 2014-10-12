__author__ = 'ipetrash'


"""Модуль для возвращения информации о томе ранобе."""


from grab import Grab
from urllib.parse import urljoin
from urllib.parse import urlparse
import os.path


def get_volume_base_page(url):
    """Функция возвратит базовую страницу url, например для
    http://ruranobe.ru/r/mknr/v12/ch1 вернется ch1,
    а для http://ruranobe.ru/r/mknr/v8/a?action=edit&redlink=1
    будет возвращено a."""

    path = urlparse(url).path
    base_url = os.path.basename(path)
    return base_url


# Типы страниц в томе:
#   i   - Начальные иллюстрации
#   p1  - Вступление
#   p2  - Пролог
#   ch% - Глава %
#   e   - Эпилог
#   a   - Послесловие
#   a2  - Запоздавший шедевр
#   at  - Послесловие команды перевода


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

    # TODO: Обернуть в функцию код получения полной ссылки к картинке обложки, в функцию передавать только адрес тома
    # Относительная ссылка к обложки тома
    relative_url_cover = g.doc.select('//td[@id="cover"]/a').attr('href')

    # Соединение адреса к главной странице ранобе и относительной ссылки к обложке тома
    url_cover_volume = urljoin(url_ranobe, relative_url_cover)

    grab_cover = Grab()
    g.setup(hammer_mode=True)
    grab_cover.go(url_cover_volume)
    relative_url_cover = grab_cover.doc.select('//div[@class="fullImageLink"]/a').attr('href')

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

    # Словарь содержит информацию о томе
    info = {
        "name": volume_name,
        "series": series,
        "author": author,
        "illustrator": illustrator,
        "ISBN": volume_isbn,
        "url_cover": url_cover_volume,
        "chapters": chapters,
    }

    for ch in contents:
        # Адрес к главе тома
        url_chapter = urljoin(url_ranobe, ch.attr("href"))

        # Проверка на существование страницы с главой
        grab_chapter = Grab()
        grab_chapter.setup(hammer_mode=True)
        grab_chapter.go(url_chapter)

        # Тип страницы тома может быть "Начальные иллюстрации", "Пролог", сами главы, и т.п.
        # Типы страниц описаны выше данной функции.
        volume_base_page = get_volume_base_page(url_chapter)

        # Послесловие команды перевода не относится напрямую к ранобе, поэтому оно не будет включено
        if volume_base_page == "at":
            continue

        # Тут мы проверяем наличие глав тома: если не удачно, выходим из функции, без возврата тома
        if grab_chapter.response.code != 200:
            # TODO: кажется, лучше выкидывать исключения с описанием причины
            print("Не найдена глава: {}".format(url_chapter))

            # Если типом является глава, выходим -- нам не нужен том, у которого будут отсутствовать
            # какие то главы, а вот все остальным ("Начальные иллюстрации", "Пролог", "Эпилог",
            # "Послесловие", и т.п.) можно пренебречь
            if volume_base_page.startswith("ch"):
                return

            # Пропускаем добавление страницы в список
            continue

        # Разбиение списка глав соответственно с типами страниц: главы -- отдельно, а все остальное тоже отдельно.

        # Если типом страницы является глава:
        if volume_base_page.startswith("ch"):
            # Добавление адреса главы к списку
            chapters.append(url_chapter)
        else:
            # Добавляем в словарь типа страниц
            info[volume_base_page] = url_chapter

    return info