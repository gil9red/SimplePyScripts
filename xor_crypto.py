#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from itertools import cycle


def crypto_xor_1(message: str, secret: int) -> str:
    """
    Каждый символ xor'ится одним числом.
    Уязвимо для частотного анализа.

    """

    return "".join(chr(ord(c) ^ secret) for c in message)


def crypto_xor_2(message: str, secret: str) -> str:
    """
    Каждый символ xor'ится последовательно каждым символом из secret.
    Уязвимо для частотного анализа.

    """

    new_chars = list()

    for num_chr in (ord(c) for c in message):
        for num_secret_char in (ord(c) for c in secret):
            num_chr ^= num_secret_char

        new_chars.append(num_chr)

    return "".join(chr(c) for c in new_chars)


def crypto_xor_3(message: str, secret: str) -> str:
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

    return "".join(chr(c) for c in new_chars)


# NOTE: Аналог crypto_xor_3
def crypto_xor_4(message: str, secret: str) -> str:
    """
    Символы из message и secret xor'ятся последовательно: message[i] ^ secret[i] и когда
    длина secret заканчивается, счетчик сбрасывается и xor продолжается: message[i] ^ secret[j]

    Если secret меньше message, тогда частоты символов шифрованного сообщения распределяются,
    т.к. в этом случае один и тот же символ из message может принять в шифрованном сообщение
    разные значения (зависит от того на какой символ из secret попадет).

    """

    return "".join(chr(ord(c) ^ ord(k)) for c, k in zip(message, cycle(secret)))


def encrypt_xor_hex(message: str, secret: str) -> str:
    """
    Результатом шифрования будет HEX строка.

    """

    return crypto_xor_4(message, secret).encode("utf-8").hex()


def decrypt_xor_hex(message_hex: str, secret: str) -> str:
    """
    Принимает HEX строка, возвращает расшифрованную обычную строку.

    """

    message = bytes.fromhex(message_hex).decode("utf-8")
    return crypto_xor_4(message, secret)


if __name__ == "__main__":
    message = "Hello World!"
    secret_num = 50
    secret_key = "secret"

    print("secret:", secret_num)
    encrypt_text = crypto_xor_1(message, secret_num)
    print("Encrypt:", repr(encrypt_text))
    decrypt_text = crypto_xor_1(encrypt_text, secret_num)
    print("Decrypt:", decrypt_text)
    assert crypto_xor_1(crypto_xor_1(message, secret_num), secret_num) == message
    print()

    print("secret:", secret_key)
    encrypt_text = crypto_xor_2(message, secret_key)
    print("Encrypt:", repr(encrypt_text))
    decrypt_text = crypto_xor_2(encrypt_text, secret_key)
    print("Decrypt:", decrypt_text)
    assert crypto_xor_2(crypto_xor_2(message, secret_key), secret_key) == message
    print()

    print("secret:", secret_key)
    encrypt_text = crypto_xor_3(message, secret_key)
    print("Encrypt:", repr(encrypt_text))
    decrypt_text = crypto_xor_3(encrypt_text, secret_key)
    print("Decrypt:", decrypt_text)
    assert crypto_xor_3(crypto_xor_3(message, secret_key), secret_key) == message
    print()

    print("secret:", secret_key)
    encrypt_text = crypto_xor_4(message, secret_key)
    print("Encrypt:", repr(encrypt_text))
    decrypt_text = crypto_xor_4(encrypt_text, secret_key)
    print("Decrypt:", decrypt_text)
    assert crypto_xor_4(crypto_xor_4(message, secret_key), secret_key) == message
    print()

    print("secret:", secret_key)
    encrypt_text = encrypt_xor_hex(message, secret_key)
    print("Encrypt:", repr(encrypt_text))
    decrypt_text = decrypt_xor_hex(encrypt_text, secret_key)
    print("Decrypt:", decrypt_text)
    assert decrypt_xor_hex(encrypt_xor_hex(message, secret_key), secret_key) == message
    print()
