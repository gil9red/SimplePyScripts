import vk_api
import sys
# import requests


__author__ = 'ipetrash'


# https://github.com/python273/vk_api
# https://vk.com/dev/methods


if __name__ == '__main__':
    """ Пример работы с vk.com"""

    login, password = 'login', '******'

    try:
        vk = vk_api.VkApi(login, password)  # Авторизируемся
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)  # В случае ошибки выведем сообщение
        sys.exit()


    # ## Получение инфы о пользователе
    # # Получение инфы о текущем пользователе
    # rs = vk.method('users.get')
    #
    # # # Получение больше инфы о текущем пользователе
    # # rs = vk.method('users.get', {'fields': 'sex, city, online, screen_name'})
    #
    # # # Получение инфы о пользователе creeddevilmaycry
    # # rs = vk.method('users.get', {'user_ids': 'creeddevilmaycry'})
    # print(rs)


    ## Печатаем текст последнего поста со стены
    # values = {
    #     'count': 1  # Получаем только один пост
    # }
    # response = vk.method('wall.get', values)  # Используем метод wall.get
    #
    # if response['items']:
    #     # Печатаем текст последнего поста со стены
    #     print(response['items'][0]['text'])


    # # Получение аудизаписей текущего пользователя (чей логин был введен)
    # audio = vk.method('audio.get')
    #
    # # # Получение аудизаписей пользователя c id=170968205
    # # audio = vk.method('audio.get', {'owner_id': '170968205'})
    #
    # # Первая аудизапись пользователя
    # audio = audio['items'][0]
    # # print(audio)
    # artist = audio['artist']
    # title = audio['title']
    # url = audio['url']
    #
    # audio_file_name = '%s - %s.mp3' % (artist, title)
    #
    # # Попытаемся скачать аудизапись
    # r = requests.get(url, stream=True)
    # if r.status_code == 200:
    #     with open(audio_file_name, 'wb') as f:
    #         for chunk in r.iter_content(1024):
    #             f.write(chunk)


    # Вывод списка всех аудизаписей
    # print('Count: {}'.format(audio['count']))
    # for i, a in enumerate(audio['items'], 1):
    #     print(i, a)


    # ## Написание сообщения на стену
    # # Написание сообщения себе на стену:
    # response = vk.method('wall.post', {'message': 'Hello World! Привет Мир!'})
    # print(response)
    #
    # # Написание сообщения пользователю с id=170968205 на стену:
    # response = vk.method('wall.post', {'owner_id': '170968205', 'message': 'Даров, чувак!'})
    # print(response)


    # rs = vk.method('wall.post', {
    #     'owner_id': '4033640',
    #     'message': 'Щенята!',
    #     'attachments': 'http://doghusky.ru/wp-content/uploads/2012/02/Siberian-Husky-Puppy-Photo_002-600x375.jpg',
    # })
    # print(rs)