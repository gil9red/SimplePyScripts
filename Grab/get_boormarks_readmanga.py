"""
Скрипт, используя логин и пароль, авторизовывается, после выводит список
манга, оставленных пользователем в закладках.
"""

__author__ = "ipetrash"


from grab import Grab
import re


if __name__ == "__main__":
    username = input("Логин: ")
    password = input("Пароль: ")

    g = Grab()

    # Переходим на страницу входа
    print("...Перехожу на страницу входа...")
    g.go("http://grouple.ru/internal/auth/login")

    # Заполняем формы логина и пароля
    print("...Заполняем формы логина и пароля...")
    g.set_input("j_username", username)
    g.set_input("j_password", password)

    # Отсылаю данные
    print("...Отсылаю данные...")
    g.submit()

    # Вытаскиваем имя пользователя
    print("...Получаю имя пользователя...")
    user = g.doc.select('//a[@href="/private/index"]').text()

    # Переход на страницу Закладки
    print('...Перехожу на страницу "Закладки"...')
    g.go("http://grouple.ru/private/bookmarks")

    print(f"\nПользователь: {user}")

    # Запрос на получение всех закладок
    TEMPLATE_BOOKMARKS = (
        '//div[@class="bookmarks-lists"]/table[starts-with(@class, "cTable bookmarks_")]'
        '//tr[@class="bookmark-row"]'
    )
    # Общее количество заметок
    print("\nЗакладки({}):".format(g.doc.select(TEMPLATE_BOOKMARKS).count()))

    # Запрос на получение всех типов закладок
    TEMPLATE_TYPE_BOOKMARK = '//div[@class="bookmarks-lists"]/table[starts-with(@class, "cTable bookmarks_")]'
    type_bookmarks = g.doc.select(TEMPLATE_TYPE_BOOKMARK)

    # Регулярка для вытаскивания из имени закладки нужное
    # Например, из "Пока бросил (1)" будет вытащено: "Пока бросил"
    regexp_bookmark = re.compile(r"(.+) \(.+\)")

    # Перебор всех типов закладок
    for tb in type_bookmarks:
        bookmark = tb.select("tr/th")[1].text()  # Имя закладки с "мусором"

        # В полученной имени закладки, согласно шаблону регулярного выражения,
        # вытаскивается первая группа:
        # Например, из "Пока бросил (1)" будет вытащено: "Пока бросил"
        bookmark = regexp_bookmark.search(bookmark).group(1)
        print(f'  Закладка "{bookmark}":')

        # Получение всех закладок данного типа
        group_bookmarks = tb.select('tr[@class="bookmark-row"]')

        # Перебор всех закладок данного типа
        for bm in group_bookmarks:
            href = bm.select("td/a").attr("href")  # Ссылка на мангу
            name = bm.select("td/a/text()").text()  # Название манги
            print(f'    "{name}": {href}')

        print()
