#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path


# NOTE: Get <PEM_FILE_NAME>: openssl pkcs12 -nodes -out ipetrash.pem -in ipetrash.p12
NAME_CERT = 'ipetrash.pem'

ROOT_DIR = Path(__file__).resolve().parent
PATH_LOCAL_CERT = ROOT_DIR / NAME_CERT

DIR_CURRENT_KEYS = Path(r'C:\keys\bin\current')
PATH_COMMON_CERT = DIR_CURRENT_KEYS / NAME_CERT

if PATH_LOCAL_CERT.exists():
    PATH_CERT = PATH_LOCAL_CERT
elif PATH_COMMON_CERT.exists():
    PATH_CERT = PATH_COMMON_CERT
else:
    raise Exception(f'File {NAME_CERT} not found in: {PATH_LOCAL_CERT}, {PATH_COMMON_CERT}!')


if __name__ == '__main__':
    print(f'ROOT_DIR: {ROOT_DIR}')
    print(f'PATH_LOCAL_CERT: {PATH_LOCAL_CERT} (exists: {PATH_LOCAL_CERT.exists()})')
    print(f'PATH_COMMON_CERT: {PATH_COMMON_CERT} (exists: {PATH_COMMON_CERT.exists()})')
    print(f'PATH_CERT: {PATH_CERT} (exists: {PATH_CERT.exists()})')
