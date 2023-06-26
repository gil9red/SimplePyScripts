#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: Для смены ip нужно настроить tor
# Для этого создается torrc файл (\Data\Tor\torrc)
# И в него добавляется содержимое:
# NewCircuitPeriod 5
# MaxCircuitDirtiness 10
#
# NewCircuitPeriod 5
# MaxCircuitDirtiness 10
#
# SOCKSPort 9050
# SOCKSPort 9051
# SOCKSPort 9052
# SOCKSPort 9053


# pip install -U requests[socks]
import requests

url = 'http://httpbin.org/ip'

import sys
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
log.addHandler(handler)

while True:
    for port in [9050, 9051, 9052, 9053]:
        proxies = {
            'http': f'socks5://localhost:{port}',
            'https': f'socks5://localhost:{port}',
        }

        try:
            log.debug('port: %s, %s', port, requests.get(url, proxies=proxies).json())
        except requests.exceptions.ConnectionError:
            log.debug('port: %s, %s', port, 'WARN: Not found Tor')

    import time
    time.sleep(1)
