#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# C:\Users\<user_name>\AppData\LocalLow\Soaphog\Rezrog\Save
# C:\Users\<user_name>\AppData\LocalLow\Soaphog\Rezrog\Save\game save.json
# C:\Users\<user_name>\AppData\LocalLow\Soaphog\Rezrog\Save\progress.json

# C:\Program Files (x86)\Rezrog\Rezrog_Data\Managed\Assembly-CSharp.dll

# https://github.com/0xd4d/dnSpy/releases

# Шаги:
#   1. Скачать dnSpy https://github.com/0xd4d/dnSpy/releases
#   2. Открыть в dnSpy файл C:\Program Files (x86)\Rezrog\Rezrog_Data\Managed\Assembly-CSharp.dll
#   3. В dnSpy найти класс SaveManager
#   4. Найти ключ шифрования: private readonly string key = "32647863128053433215894456187813";
#   5. Посмотреть как игра сохраняет/загружает данные, например LoadData -> Deserialize -> Decrypt
#   6. Посмотреть как выполяется шифрование и расширование:
#         private string Encrypt(string toEncrypt)
#         {
#             byte[] bytes = Encoding.UTF8.GetBytes(this.key);
#             byte[] bytes2 = Encoding.UTF8.GetBytes(toEncrypt);
#             ICryptoTransform cryptoTransform = new RijndaelManaged
#             {
#                 Key = bytes,
#                 Mode = CipherMode.ECB,
#                 Padding = PaddingMode.PKCS7
#             }.CreateEncryptor();
#             byte[] array = cryptoTransform.TransformFinalBlock(bytes2, 0, bytes2.Length);
#             return Convert.ToBase64String(array, 0, array.Length);
#         }
#
#         private string Decrypt(string toDecrypt)
#         {
#             byte[] bytes = Encoding.UTF8.GetBytes(this.key);
#             byte[] array = Convert.FromBase64String(toDecrypt);
#             ICryptoTransform cryptoTransform = new RijndaelManaged
#             {
#                 Key = bytes,
#                 Mode = CipherMode.ECB,
#                 Padding = PaddingMode.PKCS7
#             }.CreateDecryptor();
#             byte[] bytes2 = cryptoTransform.TransformFinalBlock(array, 0, array.Length);
#             return Encoding.UTF8.GetString(bytes2);
#         }

import base64
import json

# pip install pycryptodome==3.21.0
# OR:
# pip install pycryptodomex==3.21.0
from Crypto.Cipher import AES

# pip install pkcs7==0.1.2
from pkcs7 import PKCS7Encoder


def encrypt(to_encrypt: str, key: bytes) -> bytes:
    encoder = PKCS7Encoder()
    encryptor = AES.new(key, AES.MODE_ECB)

    pad_text = encoder.encode(to_encrypt).encode("utf-8")
    cipher = encryptor.encrypt(pad_text)

    return base64.b64encode(cipher)


def decrypt(to_decrypt: bytes, key: bytes) -> str:
    encoder = PKCS7Encoder()
    encryptor = AES.new(key, AES.MODE_ECB)

    array = base64.b64decode(to_decrypt)
    decrypt_text = encryptor.decrypt(array)

    return encoder.decode(str(decrypt_text, "utf-8"))


if __name__ == "__main__":
    KEY = b"32647863128053433215894456187813"

    # C:\Users\<user_name>\AppData\LocalLow\Soaphog\Rezrog\Save
    # C:\Users\<user_name>\AppData\LocalLow\Soaphog\Rezrog\Save\game save.json
    # C:\Users\<user_name>\AppData\LocalLow\Soaphog\Rezrog\Save\progress.json

    with open("progress.json", "rb") as f:
        array = f.read()

    print(array)  # b'o41r7i6/ekDVTWAmDvsmuEwhqMelq3bF3wukSbVpeeFaKIdyX ...

    text: str = decrypt(array, KEY)
    print(text)
    # '{"goldEarnedTotal":23778,"timePlayedMage":3581.58911132813,"timePlayedArcher" ...'

    data: dict = json.loads(text)
    print(data)
    # {'goldEarnedTotal': 23778, 'timePlayedMage': 3581.58911132813, ...

    with open("progress_decrypted.json", "w", encoding="utf-8") as f:
        json.dump(data, f)

    with open("progress_decrypted_pretty.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # # Меняем данные
    # data['goldEarnedTotal'] = 9999999
    # text = json.dumps(data)
    # print(text)  # {"goldEarnedTotal": 9999999, "timePlayedMage": 16385.560546875, ...

    print()

    new_array: bytes = encrypt(text, KEY)
    print(new_array)  # b'o41r7i6/ekDVTWAmDvsmuEwhqMelq3bF3wukSbVpeeFaKIdyX ...

    with open("progress_encrypted.json", "wb") as f:
        f.write(new_array)
