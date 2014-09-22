"""
Скрипт, используя логин и пароль, авторизовывается, после выводит список
манга, оставленных пользователем в закладках.
"""

__author__ = 'ipetrash'


from grab import Grab


def get_list_bookmarks(bookmarks):
    """Функция возвращает список кортежей, в котором первым элементом
    является название манги, а вторым ссылка на нее.
    """

    l = []
    for bm in bookmarks:
        a_href = bm.select("td/a").attr('href')
        a_name = bm.select("td/a/text()").text()
        l.append((a_name, a_href))
    return l


if __name__ == '__main__':
    username = input("Логин: ")
    password = input("Пароль: ")

    g = Grab()

    # Переходим на страницу входа
    print("...Перехожу на страницу входа...")
    g.go('http://grouple.ru/internal/auth/login')

    # Заполняем формы логина и пароля
    print("...Заполняем формы логина и пароля...")
    g.set_input('j_username', username)
    g.set_input('j_password', password)

    # Отсылаю данные
    print("...Отсылаю данные...")
    g.submit()

    # Вытаскиваем имя пользователя
    print("...Получаю имя пользователя...")
    user = g.doc.select('//a[@href="/private/index"]').text()

    # Переход на страницу Закладки
    print('...Перехожу на страницу "Закладки"...')
    g.go('http://grouple.ru/private/bookmarks')

    print("\nПользователь: {}".format(user))

    print("\nЗакладки:")

    # Шаблон xpath для получения группы закладок
    TEMPLATE_BOOKMARKS = ('//div[@class="bookmarks-lists"]/table[@class="cTable bookmarks_{} "]//'
                          'tr[@class="bookmark-row"]')

    # Получение закладок "В процессе"
    watching = g.doc.select(TEMPLATE_BOOKMARKS.format("WATCHING"))
    print(" В процессе: {}".format(watching.count()))
    for name, href in get_list_bookmarks(watching):
        print('  "{}": {}'.format(name, href))

    # Получение закладок "В планах"
    planed = g.doc.select(TEMPLATE_BOOKMARKS.format("PLANED"))
    print("\n В планах: {}".format(planed.count()))
    for name, href in get_list_bookmarks(planed):
        print('  "{}": {}'.format(name, href))

    # Получение закладок "Готово"
    completed = g.doc.select(TEMPLATE_BOOKMARKS.format("COMPLETED"))
    print("\n Готово: {}".format(completed.count()))
    for name, href in get_list_bookmarks(completed):
        print('  "{}": {}'.format(name, href))