"""
Скрипт, используя логин и пароль, авторизовывается в github, после выводит список
репозиториев и некоторую информацию о них.
"""

__author__ = "ipetrash"


from grab import Grab


if __name__ == "__main__":
    login = input("Логин: ")
    password = input("Пароль: ")

    g = Grab()

    # Переходим на страницу входа
    print("...Перехожу на страницу входа...")
    g.go("https://github.com/login")

    # Заполняем формы логина и пароля
    print("...Заполняем формы логина и пароля...")
    g.set_input("login", login)
    g.set_input("password", password)

    # Отсылаю данные формы
    print("...Отсылаю данные формы...")
    g.submit()

    # Переход на страницу с репозиториями
    print("...Перехожу на страницу с репозиториями...")
    g.go("https://github.com/{}?tab=repositories".format(login))

    # Получение списка репозиториев
    print("...Получаю список репозиториев...")
    # list_repo = g.doc.select('//ul[@class="repo-list js-repo-list"]/li/h3/a')
    list_repo = g.doc.select('//h3[@class="repo-list-name"]/a')

    print(f"\nРепозитории({len(list_repo)}):")

    # Перебор всех репозиториев
    for i, repo in enumerate(list_repo, 1):
        url = "https://github.com" + repo.attr("href")
        grab_repo = Grab()
        grab_repo.go(url)  # переход на страницу репозитория

        # получение количества коммитов данного репозитория
        count = grab_repo.doc.select('//span[@class="num text-emphasized"]').text()
        print(f'{i}. "{repo.text()}" ({count} commits): {url}')
