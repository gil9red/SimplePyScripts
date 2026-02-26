#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# NOTE: Analog https://github.com/abhinavsingh/proxy.py/blob/754d5a35d28347716dfaefea91418826148ed903/Makefile#L60


import os
from config import CA_KEY_FILE_PATH, CA_CERT_FILE_PATH, CA_SIGNING_KEY_FILE_PATH


def main() -> None:
    # Generate CA key
    os.system(
        f"python -m proxy.common.pki gen_private_key --private-key-path {CA_KEY_FILE_PATH}"
    )
    os.system(
        f"python -m proxy.common.pki remove_passphrase --private-key-path {CA_KEY_FILE_PATH}"
    )

    # Generate CA certificate
    os.system(
        f"python -m proxy.common.pki gen_public_key --private-key-path {CA_KEY_FILE_PATH} "
        f"--public-key-path {CA_CERT_FILE_PATH}"
    )

    # Generate key that will be used to generate domain certificates on the fly
    # Generated certificates are then signed with CA certificate / key generated above
    os.system(
        f"python -m proxy.common.pki gen_private_key --private-key-path {CA_SIGNING_KEY_FILE_PATH}"
    )
    os.system(
        f"python -m proxy.common.pki remove_passphrase --private-key-path {CA_SIGNING_KEY_FILE_PATH}"
    )


if __name__ == "__main__":
    main()
