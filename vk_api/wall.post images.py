from grab import Grab
import urllib.parse
import re
import vk_api
import sys
import random


__author__ = 'ipetrash'


# Скрипт ищет картинки в инете и помещает на стену пользователя vk.com


if __name__ == '__main__':
    login, password = 'login', '******'

    try:
        vk = vk_api.VkApi(login, password)  # Авторизируемся
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)  # В случае ошибки выведем сообщение
        sys.exit()


    url = 'http://yandex.ru/images/search?text='
    rq_text = 'Котята'

    url += urllib.parse.quote(rq_text)

    g = Grab()
    g.go(url)

    images = g.doc.select('//a[@class="serp-item__link"]/@onmousedown')

    # Список с ссылками на картинки
    hrefs = [
        re.search(r'"href":"(.+)"', im.text()).group(1)
        for im in images
    ]

    # "Перемешаем" элементы списка
    random.shuffle(hrefs)

    # Добавление сообщения на стену пользователя 170968205
    # Если не указывать owner_id, сообщения себе на стену поместится
    for i in range(5):
        rs = vk.method('wall.post', {
            'owner_id': '170968205',
            'message': rq_text,
            'attachments': hrefs.pop(),
        })
        print(rs)