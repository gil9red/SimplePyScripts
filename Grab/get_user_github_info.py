"""
Скрипт, используя логин и пароль, авторизовывается в github, после
выводит информацию о пользователе.
"""


# TODO: добавить больше информации о пользователе.
# URL: <li class="vcard-detail" itemprop="url">


__author__ = 'ipetrash'


from grab import Grab


if __name__ == '__main__':
    login = input("Логин: ")
    password = input("Пароль: ")

    g = Grab()

    # Переходим на страницу входа
    print("...Перехожу на страницу входа...")
    g.go("https://github.com/login")

    # Заполняем формы логина и пароля
    print("...Заполняю формы логина и пароля...")
    g.set_input("login", login)
    g.set_input("password", password)

    # Отсылаю данные формы
    print("...Отсылаю данные формы...")
    g.submit()

    # Переход на страницу пользователя
    print("...Перехожу на страницу пользователя...")
    g.go("https://github.com/" + login)

    # Получение информации с страницы пользователя
    print("...Получаю информацию с страницы пользователя...")
    fullname = g.doc.select('//span[@itemprop="name"]').text()
    username = g.doc.select('//span[@itemprop="additionalName"]').text()
    organization = g.doc.select('//li[@itemprop="worksFor"]').text()
    homeLocation = g.doc.select('//li[@itemprop="homeLocation"]').text()
    email = g.doc.select('//a[@class="email"]').text()
    join_label = g.doc.select('//span[@class="join-label"]').text()
    join_title_time = g.doc.select('//time[@class="join-date"]').text()
    join_datetime = g.doc.select('//time[@class="join-date"]').attr("datetime")

    print("\nfullname:", fullname)
    print("username:", username)
    print("organization:", organization)
    print("homeLocation:", homeLocation)
    print("email:", email)
    print('{} {} ({})'.format(join_label, join_title_time, join_datetime))
