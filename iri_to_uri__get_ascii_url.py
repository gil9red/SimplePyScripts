#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urlparse, urlunparse
import re


def url_encode_non_ascii(b: bytes) -> bytes:
    return re.sub(b'[\x80-\xFF]', lambda c: b'%%%02x' % ord(c.group(0)), b)


# SOURCE: https://stackoverflow.com/a/4391299/5909792
def iri_to_uri(iri: str) -> str:
    parts = urlparse(iri)
    return urlunparse(
        part.encode('idna') if parti == 1 else url_encode_non_ascii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    ).decode('utf-8')


if __name__ == '__main__':
    url = 'https://anapa.russianrealty.ru/Продажа-квартир/'
    new_url = iri_to_uri(url)
    print(new_url)
    assert new_url == 'https://anapa.russianrealty.ru/%d0%9f%d1%80%d0%be%d0%b4%d0%b0%d0%b6%d0%b0-%d0%ba%d0%b2%d0%b0%d1%80%d1%82%d0%b8%d1%80/'

    url = 'http://www.a\u0131b.com/a\u0131b'
    new_url = iri_to_uri(url)
    print(new_url)
    assert new_url == 'http://www.xn--ab-hpa.com/a%c4%b1b'

    url = 'https://ya.ru'
    new_url = iri_to_uri(url)
    print(new_url)
    assert new_url == 'https://ya.ru'

    url = 'https://google.com'
    new_url = iri_to_uri(url)
    print(new_url)
    assert new_url == 'https://google.com'

    url = 'http://домены.рф'
    new_url = iri_to_uri(url)
    print(new_url)
    assert new_url == 'http://xn--d1acufc5f.xn--p1ai'
