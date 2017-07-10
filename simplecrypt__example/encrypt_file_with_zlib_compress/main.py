#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from simplecrypt import encrypt, decrypt
import zlib


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
    print("Compress message...")
    compress_text = zlib.compress(message)
    compress_message_digest = get_sha1_hexdigest(compress_text)
    print('Compress message len: {}, sha1: {}'.format(len(compress_text), compress_message_digest))

    print()
    print('Encrypt compress message...')
    cipher_compress_text = encrypt(PASSWORD, compress_text)
    print('Encrypt compress message len: {}'.format(len(cipher_compress_text)))

    print()
    print('Decrypt compress message...')
    decrypt_compress_message = decrypt(PASSWORD, cipher_compress_text)
    decrypt_compress_message_digest = get_sha1_hexdigest(decrypt_compress_message)
    print('Decrypt compress message len: {}, sha1: {}'.format(len(decrypt_compress_message), decrypt_compress_message_digest))

    print()
    print("Decompress message...")
    decompress_text = zlib.decompress(decrypt_compress_message)
    decompress_message_digest = get_sha1_hexdigest(decompress_text)
    print('Decompress message len: {}, sha1: {}'.format(len(decompress_text), decompress_message_digest))

    print()
    print('Digest for compress is equal: {}'.format(compress_message_digest == decrypt_compress_message_digest))
    print('Digest for message is equal: {}'.format(message_digest == decompress_message_digest))
