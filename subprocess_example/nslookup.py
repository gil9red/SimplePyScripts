#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from subprocess import Popen, PIPE
import re


def pc_name(ip):
    """Функция для получения имени компьютера по ip."""

    with Popen(['nslookup', ip], universal_newlines=True, stdout=PIPE, stderr=PIPE) as p:
        if not p.stderr.read():
            text = p.stdout.read()
            match = re.search(r'Name:(.+)', text)
            if match:
                return match.group(1).strip()


if __name__ == '__main__':
    # with open('ip_pc_name', mode='a') as f:
    #     for j in range(9):
    #         for m in range(256):
    #             ping = '{}.{}.{}.{}'.format(10, 7, j, m)
    #             name = pc_name(ping)
    #
    #             if name is not None:
    #                 found = True
    #
    #                 print(ping, name, file=f)
    #                 print(ping, name)

    # TODO: четыре цикла хотелось бы заменить одним -- должны быть инструменты в коробке
    # для генерации подобного
    with open('ip_pc_name', mode='w') as f:
        for i in range(256):
            for j in range(256):
                for k in range(256):
                    for m in range(256):
                        ping = f'{i}.{j}.{k}.{m}'
                        name = pc_name(ping)

                        if name is not None:
                            print(ping, name)
                            print(ping, name, file=f)
