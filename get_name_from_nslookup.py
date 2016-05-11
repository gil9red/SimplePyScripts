#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_ip_name(ip):
    from subprocess import Popen, PIPE
    with Popen(("nslookup", ip), shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True) as proc:
        # Дождаться выполнения
        proc.wait()

        # Получить tuple('stdout', 'stderr')
        out, err = proc.communicate()
        if err:
            return

        import re
        match = re.search('Name:(.+)', out)
        if match is not None:
            return match.group(1).strip()

        return out


if __name__ == '__main__':
    print(get_ip_name("127.0.0.1"))
    print(get_ip_name("10.7.8.33"))
    print(get_ip_name("10.7.8.31"))
    print(get_ip_name("asdasda"))
