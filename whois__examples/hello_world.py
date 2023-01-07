#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install python-whois
import whois


w = whois.whois('ru.stackoverflow.com')
print(w)
"""
{
  "domain_name": [
    "STACKOVERFLOW.COM",
    "stackoverflow.com"
  ],
  "registrar": "CSC CORPORATE DOMAINS, INC.",
  "whois_server": "whois.corporatedomains.com",
  "referral_url": null,
  "updated_date": [
    "2022-08-17 04:32:10",
    "2022-08-17 00:32:11"
  ],
  "creation_date": [
    "2003-12-26 19:18:07",
    "2003-12-26 14:18:07"
  ],
  "expiration_date": "2024-02-02 11:59:59",
  "name_servers": [
    "NS-1033.AWSDNS-01.ORG",
    "NS-358.AWSDNS-44.COM",
    "NS-CLOUD-E1.GOOGLEDOMAINS.COM",
    "NS-CLOUD-E2.GOOGLEDOMAINS.COM",
    "ns-1033.awsdns-01.org",
    "ns-358.awsdns-44.com",
    "ns-cloud-e2.googledomains.com",
    "ns-cloud-e1.googledomains.com"
  ],
  "status": [
    "clientTransferProhibited https://icann.org/epp#clientTransferProhibited",
    "clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited"
  ],
  "emails": [
    "domainabuse@cscglobal.com",
    "sysadmin-team@stackoverflow.com"
  ],
  "dnssec": "unsigned",
  "name": "Domain Administrator",
  "org": "Stack Exchange, Inc.",
  "address": "110 William Street, 28th Floor",
  "city": "New York",
  "state": "NY",
  "registrant_postal_code": "10038",
  "country": "US"
}
"""
