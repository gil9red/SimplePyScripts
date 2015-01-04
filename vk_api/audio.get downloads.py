import os
import vk_api
import sys
import requests


__author__ = 'ipetrash'


# https://github.com/python273/vk_api
# https://vk.com/dev/methods
# http://vk.com/dev/audio.getAlbums
# http://vk.com/dev/audio.get


# Download audio user
# Скачивание аудиозаписей пользователя


LOGIN, PASSWORD = '', ''
DOWNLOAD_DIR = 'downloads'


# TODO: учитывать наличие разделения песен на альбомы


def vk_auth(login, password):
    try:
        vk = vk_api.VkApi(login, password)  # Авторизируемся
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)  # В случае ошибки выведем сообщение
        sys.exit()

    return vk


def main():
    print('Авторизация...')

    # Авторизируемся
    vk = vk_auth(LOGIN, PASSWORD)

    # Получение аудиозаписей текущего пользователя (чей логин был введен)
    # Для получения аудиозаписей определенного пользователя нужно передавать
    # его id, например: audio = vk.method('audio.get', {'owner_id': '170968205'})
    audio = vk.method('audio.get')

    # # Получаем альбомы пользователя
    # albums = vk.method('audio.getAlbums')['items']
    # print(albums)
    #
    # albums = {
    #     a['id']: a['title']
    #     for a in albums
    # }
    # print(albums)

    # Если не существует пути, создадим его
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Вывод списка всех аудиозаписей
    print('Всего песен: {}'.format(audio['count']))

    for i, a in enumerate(audio['items'], 1):
        artist = a['artist']
        title = a['title']
        url = a['url']
        # duration = a['duration']
        # album_id = a.get('album_id')

        audio_name = '{} - {}'.format(artist, title)

        # Название файла аудиозаписи
        audio_file_name = audio_name + '.mp3'

        # Замена символов, которых в названиях файлов запрещено
        # TODO: бОльший контроль, индивидуальный для ОС
        audio_file_name = audio_file_name.replace('"', '')

        # Путь в который будет скачен файл
        download_path = os.path.join(DOWNLOAD_DIR, audio_file_name)

        # Попытаемся скачать аудиозапись
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            print('{}. "{}"'.format(i, audio_name), end='')

            # Создаем файл и в него записываем файл с сервера
            with open(download_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

            print(' download finished...')

        else:
            print('Не получилось скачать "{}"...'.format(audio_name))


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print('\n\nСкачивание прервано.')
        sys.exit()