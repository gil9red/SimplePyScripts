"""
"""

__author__ = 'ipetrash'


from grab import Grab
from grab import UploadFile


if __name__ == '__main__':
    g = Grab()
    h = {
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'User-Agent': ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')
    }
    g.go('http://rghost.ru/', headers=h)
    print(g.response.url)
    # Получим ссылку на сервер файлообменника
    url = g.doc.select('//form[@enctype="multipart/form-data"]').attr("action")
    print(url)
    # g.setup(multipart_post={'file': UploadFile('im.png')}, headers=h)
    # g.go(url)
    # print(g.response.url)

    # TODO: http://gyazo.com/2bb1828cb1c14d99cf66e6133508a4bd
    # g = Grab()
    # headers = {'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'}
    # g.go('http://rghost.ru/', headers=headers)
    # g.choose_form_by_element('upload_form')
    # g.set_input('file', UploadFile('im.png'))
    # # g.submit()
    # print(g.response.url)

    # import re
    # g = Grab()
    # g.go('http://rghost.ru/')
    # # Выдираем сервер для заливки файла, тут url = 'http://pion.rghost.net/files'
    # url = re.findall(r"action=\"(http.+?)\"\senctype=\"mul", g.response.body, re.S)[0]
    # g.setup(multipart_post={'file': UploadFile('im.png')})  # Подготавливаем запрос
    # g.go(url)  # Отправляем запрос
    # print(g.response.url)  # http://rghost.net/ ...