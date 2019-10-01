# RSA helper class for pycrypto
# Copyright (c) Dennis Lee
# Date 21 Mar 2017
#
# Copyright (c) 2019 gil9red <https://github.com/gil9red/>

# Description:
# Python helper class to perform RSA encryption, decryption, 
# signing, verifying signatures & keys generation

# Dependencies Packages:
# pycrypto 

# Documentation:
# https://www.dlitz.net/software/pycrypto/api/2.6/

# Sample usage:
"""
import rsa
from base64 import b64encode, b64decode

msg1 = "Hello Tony, I am Jarvis!"
msg2 = "Hello Toni, I am Jarvis!"
key_size = 2048
public, private = rsa.new_keys(key_size)
encrypted = b64encode(rsa.encrypt(msg1, private))
decrypted = rsa.decrypt(b64decode(encrypted), private)
signature = b64encode(rsa.sign(msg1, private, "SHA-512"))
verify = rsa.verify(msg1, b64decode(signature), public)

print(private.exportKey('PEM'))
print(public.exportKey('PEM'))
print("Encrypted: " + encrypted)
print("Decrypted: '%s'" % decrypted)
print("Signature: " + signature)
print("Verify: %s" % verify)
rsa.verify(msg2, b64decode(signature), public)
"""


from typing import Union, Any, Tuple, ByteString

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random


DEFAULT_KEY_SIZE = 2048
DEFAULT_HASH_ALG = "SHA-256"


def _get_hash(hash_alg: str = DEFAULT_HASH_ALG) -> Any:
    if hash_alg == "SHA-512":
        digest = SHA512.new()
    elif hash_alg == "SHA-384":
        digest = SHA384.new()
    elif hash_alg == "SHA-256":
        digest = SHA256.new()
    elif hash_alg == "SHA-1":
        digest = SHA.new()
    else:
        digest = MD5.new()

    return digest


def new_keys(key_size: int = DEFAULT_KEY_SIZE) -> Tuple['RsaKey', 'RsaKey']:
    random_generator = Random.new().read
    key = RSA.generate(key_size, random_generator)
    private, public = key, key.publickey()
    return public, private


def import_key(extern_key: Union[str, bytes]) -> 'RsaKey':
    return RSA.importKey(extern_key)


def get_public_key(private_key: 'RsaKey') -> 'RsaKey':
    return private_key.publickey()


def encrypt(message: ByteString, pub_key: 'RsaKey') -> bytes:
    # RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)


def decrypt(cipher_text: ByteString, private_key: 'RsaKey') -> bytes:
    # RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(cipher_text)


def sign(message: bytes, private_key: 'RsaKey', hash_alg: str = DEFAULT_HASH_ALG) -> bytes:
    digest = _get_hash(hash_alg)
    digest.update(message)

    signer = PKCS1_v1_5.new(private_key)
    return signer.sign(digest)


def verify(message: bytes, signature: bytes, pub_key: 'RsaKey', hash_alg: str = DEFAULT_HASH_ALG) -> bool:
    digest = _get_hash(hash_alg)
    digest.update(message)

    signer = PKCS1_v1_5.new(pub_key)
    return signer.verify(digest, signature)
