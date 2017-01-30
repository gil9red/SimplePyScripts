#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from config import *

    from qbittorrent import Client
    qb = Client(IP_HOST)
    qb.login(USER, PASSWORD)

    # data = open('[rutor.is]Homeland_Season_06.torrent', "r", encoding='latin1').read()
    url = 'http://anti-tor.org/download/544942'

    last_number_files = 0

    while True:
        from datetime import datetime
        today = datetime.today()
        print('{}: Проверка http://anti-tor.org/torrent/544942 / {}'.format(today, url))

        while True:
            try:
                import requests
                data = requests.get(url).content.decode('latin1')

                import effbot_bencode
                torrent = effbot_bencode.decode(data)

                break

            except:
                import traceback
                print(traceback.format_exc())

                # Если произошла какая-то ошибка попытаемся через 30 секунд попробовать снова
                import time
                time.sleep(30)

        files = ["/".join(file["path"]) for file in torrent["info"]["files"]]
        if len(files) != last_number_files:
            print('Обнаружены изменения: {} файлов, {} фильмов: {}'.format(
                len(files),
                len(list(filter(lambda x: x.endswith('.avi'), files))),
                files
            ))
            last_number_files = len(files)

            qb.download_from_link('http://anti-tor.org/download/544942')
        else:
            print('Изменений нет')

        print()

        # Every 3 hours
        from datetime import timedelta
        today = datetime.today()
        timeout_date = today + timedelta(hours=3)

        while today <= timeout_date:
            def str_timedelta(td):
                mm, ss = divmod(td.seconds, 60)
                hh, mm = divmod(mm, 60)
                return "%d:%02d:%02d" % (hh, mm, ss)

            left = timeout_date - today
            left = str_timedelta(left)

            print('\r' * 50, end='')
            print('До следующего запуска осталось {}'.format(left), end='')

            import sys
            sys.stdout.flush()

            # Delay 1 seconds
            import time
            time.sleep(1)
            today = datetime.today()

        print('\r' * 50, end='')
        print('\n')
