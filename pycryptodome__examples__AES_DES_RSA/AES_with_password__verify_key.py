#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import hashlib

# pip install pycryptodome
# OR:
# pip install pycryptodomex
from Crypto.Cipher import AES


class AuthenticationError(Exception):
    pass


class CryptoAES:
    def __init__(self, key: str):
        self.key = hashlib.sha256(key.encode("utf-8")).digest()

    def encrypt(self, plain_text: str) -> str:
        data = plain_text.encode("utf-8")

        cipher = AES.new(self.key, AES.MODE_EAX)
        cipher_text, tag = cipher.encrypt_and_digest(data)
        encrypted_data = cipher.nonce + tag + cipher_text

        return base64.b64encode(encrypted_data).decode("utf-8")

    def decrypt(self, encrypted_text: str) -> str:
        encrypted_data = base64.b64decode(encrypted_text)

        nonce, tag, cipher_text = (
            encrypted_data[:16],
            encrypted_data[16:32],
            encrypted_data[32:],
        )
        cipher = AES.new(self.key, AES.MODE_EAX, nonce)

        try:
            data = cipher.decrypt_and_verify(cipher_text, tag)
        except ValueError as e:
            raise AuthenticationError(e)

        return data.decode("utf-8")


if __name__ == "__main__":
    text = "Hello World!"
    password = "123"

    crypto = CryptoAES(password)
    encrypted_text = crypto.encrypt(text)

    print(encrypted_text)
    print(crypto.decrypt(encrypted_text))
    assert text == crypto.decrypt(encrypted_text)

    # Decrypt with invalid password
    try:
        CryptoAES("abc").decrypt(encrypted_text)
    except AuthenticationError as e:
        assert str(e) == "MAC check failed"
