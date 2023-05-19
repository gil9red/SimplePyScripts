from grab import Grab

"""Скрипт, используя логин и пароль, авторизовывается в github, после выводит
информацию о пользователе.
"""


__author__ = "ipetrash"


if __name__ == "__main__":
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
    avatar = g.doc.select(
        '//*[@class="vcard-avatar tooltipped tooltipped-s"]/*[@class="avatar"]'
    ).attr("src")
    organization = g.doc.select('//li[@itemprop="worksFor"]').text()
    homeLocation = g.doc.select('//li[@itemprop="homeLocation"]').text()
    email = g.doc.select('//a[@class="email"]').text()
    url = g.doc.select('//li[@itemprop="url"]').text()
    join_label = g.doc.select('//span[@class="join-label"]').text()
    join_title_time = g.doc.select('//time[@class="join-date"]').text()
    join_datetime = g.doc.select('//time[@class="join-date"]').attr("datetime")

    print()
    print("full name:", fullname)
    print("user name:", username)
    print("avatar:", avatar)
    print("organization:", organization)
    print("home location:", homeLocation)
    print("email:", email)
    print("url:", url)
    print(f"{join_label} {join_title_time} ({join_datetime})")

    # Получение списка репозиториев
    print()
    print("...Перехожу на вкладку репозиториев...")
    g.go("https://github.com/" + login + "?tab=repositories")

    print("...Получаю список репозиториев...")
    list_source_repo = g.doc.select('//li[@class="repo-list-item public source"]')

    print()
    print("Репозитории:")
    print(f"Sources({len(list_source_repo)}):")

    for i, repo in enumerate(list_source_repo, 1):
        name = repo.select('*[@class="repo-list-name"]/a')

        href = "https://github.com" + name.attr("href")
        print(f"  {i}. {name.text()}: {href}")

        description = repo.select('*[@class="repo-list-description"]')
        if description.count():
            print(f'      "{description.text()}"')

        stats = repo.select('*[@class="repo-list-stats"]').text().split(" ")
        lang, stars, forks = stats
        print(f"      lang: {lang}, stars: {stars}, forks: {forks}\n")
