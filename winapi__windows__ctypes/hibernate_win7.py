#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'
 
 
"""Скрипт отправляет win7 в режим гибернации (спящий режим)"""
 

try:
    import sys
    if len(sys.argv) > 1:
        seconds_delay = int(sys.argv[1])

        import time

        while seconds_delay > 0:
            print(f'\rDelay before hibernate: {seconds_delay} secs', end='')
            time.sleep(1)
            seconds_delay -= 1

    print('\nGo to Hibernate')

    # Для включения режима гибернации нужно запустить консоль от администратора и ввести:
    # powercfg -hibernate on

    import os
    os.system('rundll32 powrprof.dll,SetSuspendState 0,1,0')

except KeyboardInterrupt:
    print('\nInterrupt')
