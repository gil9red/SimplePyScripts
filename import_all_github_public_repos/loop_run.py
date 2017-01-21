#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


while True:
    from datetime import datetime
    today = datetime.today()
    print(today)
    print()

    from main import run
    run()

    print('\n\n' + '-' * 20 + '\n\n')

    # Every 12 hours
    from datetime import timedelta
    today = datetime.today()
    timeout_date = today + timedelta(hours=12)

    while today <= timeout_date:
        print('\r' * 50, end='')
        print('До следующего запуска осталось {}'.format(timeout_date - today), end='')

        import sys
        sys.stdout.flush()

        # Delay 10 seconds
        import time
        time.sleep(10)

        today = datetime.today()

    print('\n')
