#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'
 
 
"""Скрипт отправляет win7 в режим гибернации (спящий режим)"""
 
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        seconds_delay = sys.argv[1]
        print('Delay before hibernate: {} secs'.format(seconds_delay))

        import time
        time.sleep(float(seconds_delay))

    print('Go to Hibernate')

    import os
    os.system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
