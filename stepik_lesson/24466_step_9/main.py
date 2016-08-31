#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from simplecrypt import decrypt, DecryptionException

    with open("encrypted.bin", "rb") as f:
        encrypted_bin = f.read()

        with open('passwords.txt') as f:
            for password in f.read().splitlines():
                try:
                    plaintext = decrypt(password, encrypted_bin)
                    print('Yes! Message is "{}".'.format(plaintext.decode()))

                except DecryptionException:
                    print('Password "{}" has not approached'.format(password))
