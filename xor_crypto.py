#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def crypto(message, secret):
    new_chars = list()

    for num_chr in (ord(c) for c in message):
        if type(secret) == int:
            num_chr ^= secret

        else:
            for num_secret_char in (ord(c) for c in secret):
                num_chr ^= num_secret_char

        new_chars.append(num_chr)

    return ''.join(chr(c) for c in new_chars)


if __name__ == '__main__':
    message = 'Hello World!'

    secret = 'secret'
    print('secret:', secret)
    encrypt_text = crypto(message, secret)
    print('Encrypt:', encrypt_text)

    decrypt_text = crypto(encrypt_text, secret)
    print('Decrypt:', decrypt_text)

    print()

    secret = 50
    print('secret:', secret)
    encrypt_text = crypto(message, secret)
    print('Encrypt:', encrypt_text)

    decrypt_text = crypto(encrypt_text, secret)
    print('Decrypt:', decrypt_text)
