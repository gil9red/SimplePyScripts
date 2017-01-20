#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


while True:
    from datetime import datetime
    today = datetime.today()
    print(today)
    print()

    from main import main
    main()

    print('\n\n' + '-' * 20 + '\n\n')

    # Every 12 hours
    from datetime import timedelta
    while today <= today + timedelta(hours=12):
        # Delay 5 minutes
        import time
        time.sleep(5 * 60)

        today = datetime.today()
