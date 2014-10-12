__author__ = 'ipetrash'


"""Модуль для возвращения информации о ранобе."""


def ranobe_info():
    """Функция возвращает словарь, содержащий информацию о ранобе."""

    from grab import Grab
    url = 'http://ruranobe.ru/r/mknr'

    g = Grab()
    g.setup(hammer_mode=True)
    g.go(url)

    # Если не удачно, выходим
    if g.response.code != 200:
        print("Не найден {}.".format(url))
        return

    # Получение основного контекста, содержащий аннотацию и ссылки на тома
    content_text = g.doc.select('//div[@id="mw-content-text"]')

    # Получение названия ранобе
    name_ranobe = g.doc.select('//h1[@id="firstHeading"]').text()

    # Получение и объединение параграфов в единый текст
    annotation = '\n'.join(r.text() for r in content_text.select('p/i'))

    # Получение списка томов
    list_volumes = content_text.select('ul/li/a')

    info = {
        "name": name_ranobe,
        "annotation": annotation,
        "list_volumes": list_volumes,
        "url": url,
    }
    return info