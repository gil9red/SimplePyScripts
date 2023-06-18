#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://en.wikipedia.org/wiki/Magnet_URI_scheme
# https://ru.wikipedia.org/wiki/Magnet-ссылка


from urllib.parse import urlparse, parse_qs


def parse(url: str) -> dict:
    result = urlparse(url)
    return parse_qs(result.query)


if __name__ == "__main__":
    import json

    links = [
        "magnet:?xt=urn:btih:19270c27523f428d6b9d23c264e4a0ff57869275&dn=rutor.info_%D0%94%D0%BE%D0%BA%D1%82%D0%BE%D1%80+%D0%A8%D0%B0%D0%BD%D1%81+%2F+Chance+%5B02x01-04+%D0%B8%D0%B7+10%5D+%282017%29+WEB-DLRip+1080p+%7C+Profix+Media&tr=udp://opentor.org:2710&tr=udp://opentor.org:2710&tr=http://retracker.local/announce",
        "magnet:?xt=urn:btih:1ff5a51d2f65e7c2fa200ada0896075543398a73&dn=rutor.info_Heroes+%26+Generals+%5B12.10.17%5D+%282016%29+PC+%7C+Online-only&tr=udp://opentor.org:2710&tr=udp://opentor.org:2710&tr=http://retracker.local/announce",
        "magnet:?xt=urn:btih:08c3a30e88b38ccf6926c073ecd41f983cbf2b20&dn=rutor.info_%D0%A4%D0%B8%D0%B7%D1%80%D1%83%D0%BA+%5B04%D1%8501-10+%D0%B8%D0%B7+21%5D+%282017%29+HDTVRip-AVC+%D0%BE%D1%82+GeneralFilm&tr=udp://opentor.org:2710&tr=udp://opentor.org:2710&tr=http://retracker.local/announce",
        "magnet:?xl=10826029&dn=mediawiki-1.15.1.tar.gz&xt=urn:sha1:XRX2PEFXOOEJFRVUCX6HMZMKS5TWG4K5&as=https%3A%2F%2Freleases.wikimedia.org%2Fmediawiki%2F1.15%2Fmediawiki-1.15.1.tar.gz",
    ]

    pretty = lambda data: json.dumps(data, indent=4, ensure_ascii=False)

    for i, link in enumerate(links, 1):
        data = parse(link)
        print("{}.\n{}\n".format(i, pretty(data)))
