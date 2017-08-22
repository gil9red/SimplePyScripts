#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def crypto_xor_1(message, secret):
    """
    Каждый символ xor'ится одним числом.
    Уязвимо для частотного анализа.

    """

    return ''.join(chr(ord(c) ^ secret) for c in message)


def crypto_xor_2(message, secret):
    """
    Каждый символ xor'ится последовательно каждым символом из secret.
    Уязвимо для частотного анализа.

    """

    new_chars = list()

    for num_chr in (ord(c) for c in message):
        for num_secret_char in (ord(c) for c in secret):
            num_chr ^= num_secret_char

        new_chars.append(num_chr)

    return ''.join(chr(c) for c in new_chars)


def crypto_xor_3(message, secret):
    """
    Символы из message и secret xor'ятся последовательно: message[i] ^ secret[i] и когда
    длина secret заканчивается, счетчик сбрасывается и xor продолжается: message[i] ^ secret[j]

    Если secret меньше message, тогда частоты символов шифрованного сообщения распределяются,
    т.к. в этом случае один и тот же символ из message может принять в шифрованном сообщение
    разные значения (зависит от того на какой символ из secret попадет).

    """

    new_chars = list()
    i = 0

    for num_chr in (ord(c) for c in message):
        num_chr ^= ord(secret[i])
        new_chars.append(num_chr)

        i += 1
        if i >= len(secret):
            i = 0

    return ''.join(chr(c) for c in new_chars)


if __name__ == '__main__':
    message = 'Hello World!'

    secret = 50
    print('secret:', secret)
    encrypt_text = crypto_xor_1(message, secret)
    print('Encrypt:', repr(encrypt_text))

    decrypt_text = crypto_xor_1(encrypt_text, secret)
    print('Decrypt:', decrypt_text)

    print()

    secret = 'secret'
    print('secret:', secret)
    encrypt_text = crypto_xor_2(message, secret)
    print('Encrypt:', repr(encrypt_text))

    decrypt_text = crypto_xor_2(encrypt_text, secret)
    print('Decrypt:', decrypt_text)

    print()

    secret = 'secret'
    print('secret:', secret)
    encrypt_text = crypto_xor_3(message, secret)
    print('Encrypt:', repr(encrypt_text))

    decrypt_text = crypto_xor_3(encrypt_text, secret)
    print('Decrypt:', decrypt_text)
