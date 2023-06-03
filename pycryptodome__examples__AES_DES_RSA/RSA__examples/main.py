#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/42856051/5909792
# SOURCE: https://gist.github.com/dennislwy/0194036234445776d48ad2fb594457d4


from base64 import b64encode, b64decode
import rsa


msg1 = "Hello Tony, I am Jarvis!".encode("utf-8")
msg2 = "Hello Toni, I am Jarvis!".encode("utf-8")

public, private = rsa.new_keys(key_size=2048)
print("private:", private.exportKey("PEM"))
print("public:", public.exportKey("PEM"))
print()

# Encrypt-Decrypt: private -> private
encrypted = b64encode(rsa.encrypt(msg1, private))
print("Encrypted:", encrypted)

decrypted = rsa.decrypt(b64decode(encrypted), private)
print("Decrypted:", decrypted)
print()

signature = b64encode(rsa.sign(msg1, private))
print("Signature:", signature)
print()

verify = rsa.verify(msg1, b64decode(signature), private)
print("Verify:", verify)  # True

verify = rsa.verify(msg2, b64decode(signature), private)
print("Verify:", verify)  # False
# Encrypt-Decrypt: private -> private

print("\n")

# Encrypt-Decrypt: public -> private
encrypted = b64encode(rsa.encrypt(msg1, public))
print("Encrypted:", encrypted)

decrypted = rsa.decrypt(b64decode(encrypted), private)
print("Decrypted:", decrypted)
print()

# TODO: signature with public don't working
# signature = b64encode(rsa.sign(msg1, public))
# print("Signature:", signature)
# print()

verify = rsa.verify(msg1, b64decode(signature), public)
print("Verify:", verify)  # True

verify = rsa.verify(msg2, b64decode(signature), public)
print("Verify:", verify)  # False
# Encrypt-Decrypt: public -> private
