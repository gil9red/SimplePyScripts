#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/60804101/5909792


from OpenSSL import crypto


def cert_gen(
    email_address="emailAddress",
    common_name="commonName",
    country_name="NT",
    locality_name="localityName",
    state_or_province_name="stateOrProvinceName",
    organization_name="organizationName",
    organization_unit_name="organizationUnitName",
    serial_number=0,
    validity_end_in_seconds=10 * 365 * 24 * 60 * 60,
    key_file="key.pem",
    cert_file="cert.pem"
):
    # Create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    # Create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = country_name
    cert.get_subject().ST = state_or_province_name
    cert.get_subject().L = locality_name
    cert.get_subject().O = organization_name
    cert.get_subject().OU = organization_unit_name
    cert.get_subject().CN = common_name
    cert.get_subject().emailAddress = email_address
    cert.set_serial_number(serial_number)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validity_end_in_seconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')

    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


if __name__ == '__main__':
    cert_gen()
