#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib

# pip install pycryptodome
# OR:
# pip install pycryptodomex
from Crypto.Cipher import AES
from Crypto import Random


# SOURCE: https://github.com/maldevel/gdog/blob/a3a47b17231d0ee3a2d0fa8ac986f7485f3f6b82/gdog.py#L68
class InfoSecurity:
    def __init__(self, key: str | bytes):
        if isinstance(key, str):
            key = key.encode("utf-8")

        self.bs = 32
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, plain_text: bytes) -> bytes:
        raw = self._pad(plain_text)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, cipher_text: bytes) -> bytes:
        enc = cipher_text
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size :]))

    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/82810f8397907679316107f135a5b1dd1fcca516/pad__unpad__example.py#L7
    def _pad(self, s: bytes) -> bytes:
        pad_size = self.bs - (len(s) % self.bs)
        return s + bytes([pad_size] * pad_size)

    @staticmethod
    def _unpad(s: bytes) -> bytes:
        pad_size = s[-1]
        return s[:-pad_size]


if __name__ == "__main__":
    AES_key = "<my AES key>"
    info_sec = InfoSecurity(AES_key)

    text = b"Hello World!"
    cipher_text = info_sec.encrypt(text)
    print(cipher_text)
    assert info_sec.decrypt(cipher_text) == text
