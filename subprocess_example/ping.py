#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from subprocess import Popen, PIPE, STDOUT
import re


ping_res = Popen("ping ya.ru", stdout=PIPE, stderr=STDOUT)

text = ''
for line in ping_res.stdout.readlines():
    text += line.decode('cp866')

print(text)
# Обмен пакетами с ya.ru [87.250.250.242] с 32 байтами данных:
# Ответ от 87.250.250.242: число байт=32 время=26мс TTL=54
# Ответ от 87.250.250.242: число байт=32 время=26мс TTL=54
# Ответ от 87.250.250.242: число байт=32 время=26мс TTL=54
# Ответ от 87.250.250.242: число байт=32 время=26мс TTL=54
#
# Статистика Ping для 87.250.250.242:
#     Пакетов: отправлено = 4, получено = 4, потеряно = 0
#     (0% потерь)
# Приблизительное время приема-передачи в мс:
#     Минимальное = 26мсек, Максимальное = 26 мсек, Среднее = 26 мсек

items = re.findall(r'TTL=(\d+)', text)
print(items)
# ['54', '54', '54', '54']

m = re.search(r'Пакетов: отправлено = (\d+), получено = (\d+), потеряно = (\d+)', text)
if m:
    print(m.groups())
    # ('4', '4', '0')
