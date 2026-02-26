#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import hashlib

# pip install pycryptodome
# OR:
# pip install pycryptodomex
from Crypto.Cipher import AES
from Crypto import Random


AES_key = "<my AES key>"


# SOURCE: https://github.com/maldevel/gdog/blob/a3a47b17231d0ee3a2d0fa8ac986f7485f3f6b82/gdog.py#L68
class InfoSecurity:
    def __init__(self, key: str) -> None:
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text: str) -> str:
        raw = self._pad(plain_text.encode("utf-8"))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, cipher_text: str) -> str:
        enc = base64.b64decode(cipher_text)
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")

    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/82810f8397907679316107f135a5b1dd1fcca516/pad__unpad__example.py#L7
    def _pad(self, s: bytes) -> bytes:
        pad_size = self.bs - (len(s) % self.bs)
        return s + bytes([pad_size] * pad_size)

    @staticmethod
    def _unpad(s: bytes) -> bytes:
        pad_size = s[-1]
        return s[:-pad_size]


if __name__ == "__main__":
    info_sec = InfoSecurity(AES_key)

    text = "Hello World!"
    cipher_text = info_sec.encrypt(text)
    print(cipher_text)
    assert info_sec.decrypt(cipher_text) == text

    text = "Привет Мир!"
    cipher_text = info_sec.encrypt(text)
    print(cipher_text)
    assert info_sec.decrypt(cipher_text) == text
