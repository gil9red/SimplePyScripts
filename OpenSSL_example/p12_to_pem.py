#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
from OpenSSL import crypto


def save_pem(p12_file_name, p12_password, pem_file_name=None) -> None:
    """Функция из p12 вытаскивает pem. Если pem_file_name не указан,
    сохраняется в той же папке, что и p12_file_name."""

    if pem_file_name is None:
        pem_file_name = os.path.splitext(p12_file_name)[0] + ".pem"

    # May require "" for empty password depending on version
    p12 = crypto.load_pkcs12(open(p12_file_name, "rb").read(), p12_password)

    with open(pem_file_name, mode="wb") as f:
        # PEM formatted private key
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))

        # PEM formatted certificate
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()))


if __name__ == "__main__":
    p12_file_name = ""
    p12_password = ""
    save_pem(p12_file_name, p12_password)
