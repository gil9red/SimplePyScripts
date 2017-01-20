#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


while True:
    from datetime import datetime
    print(datetime.today())
    print()

    from main import main
    main()

    print('\n\n' + '-' * 20 + '\n\n')

    # Every 12 hours
    import time
    time.sleep(60 * 60 * 12)
