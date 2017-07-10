#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from simplecrypt import encrypt, decrypt


def get_sha1_hexdigest(data):
    import hashlib
    sha1 = hashlib.sha1(data)
    return sha1.hexdigest()


PASSWORD = "secret"
FILENAME = "message.txt"


if __name__ == '__main__':
    print("Reading message...")
    message = open('message.txt', mode='rb').read()
    message_digest = get_sha1_hexdigest(message)
    print('Message len: {}, sha1: {}'.format(len(message), message_digest))

    print()
    print('Encrypt message...')
    cipher_text = encrypt(PASSWORD, message)
    print('Encrypt message len: {}'.format(len(cipher_text)))

    print()
    print('Decrypt message...')
    decrypt_message = decrypt(PASSWORD, cipher_text)
    decrypt_message_digest = get_sha1_hexdigest(message)
    print('Decrypt message len: {}, sha1: {}'.format(len(decrypt_message), decrypt_message_digest))

    print()
    print('Digest is equal: {}'.format(message_digest == decrypt_message_digest))
