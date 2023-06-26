#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Алиса владеет интересной информацией, которую хочет заполучить Боб.
Алиса умна, поэтому она хранит свою информацию в зашифрованном файле.
У Алисы плохая память, поэтому она хранит все свои пароли в открытом виде в текстовом файле.

Бобу удалось завладеть зашифрованным файлом с интересной информацией и файлом с паролями, но он не смог понять
какой из паролей ему нужен. Помогите ему решить эту проблему.

Алиса зашифровала свою информацию с помощью библиотеки simple-crypt.
Она представила информацию в виде строки, и затем записала в бинарный файл результат работы метода simplecrypt.encrypt.

Вам необходимо установить библиотеку simple-crypt, и с помощью метода simplecrypt.decrypt узнать, какой из паролей
служит ключом для расшифровки файла с интересной информацией.

Ответом для данной задачи служит расшифрованная интересная информация Алисы.
"""


if __name__ == '__main__':
    from simplecrypt import decrypt, DecryptionException

    with open("encrypted.bin", "rb") as f:
        encrypted_bin = f.read()

        with open('passwords.txt') as f:
            for password in f.read().splitlines():
                try:
                    plaintext = decrypt(password, encrypted_bin)
                    print(f'Yes! Message is "{plaintext.decode()}".')

                except DecryptionException:
                    print(f'Password "{password}" has not approached')
