#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://quasiocculti.com/blog/user-agent-botov-poiskovyh-sistem


GOOGLE = [
    "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)",
    "Mediapartners-Google",
    "Mozilla/5.0 (Linux; Android 5.0; SM-G920A) AppleWebKit (KHTML, like Gecko) Chrome Mobile Safari "
    "(compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 "
    "Mobile/13B143 Safari/601.1 (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)",
    "AdsBot-Google (+http://www.google.com/adsbot.html)",
    "Googlebot-Image/1.0",
    "Googlebot-News",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mediapartners-Google/2.1; +http://www.google.com/bot.html",
    "AdsBot-Google-Mobile-Apps",
]

YANDEX = [
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 "
    "Mobile/12B411 Safari/600.1.4 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexAccessibilityBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 "
    "Mobile/12B411 Safari/600.1.4 (compatible; YandexMobileBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexDirectDyn/1.0; +http://yandex.com/bots",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 "
    "(compatible; YandexScreenshotBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexVideo/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexVideoParser/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexMedia/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexBlogs/0.99; robot; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexFavicons/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexWebmaster/2.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexPagechecker/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexImageResizer/2.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexAdNet/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexDirect/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YaDirectFetcher/1.0; Dyatel; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexCalendar/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexSitelinks; Dyatel; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexMetrika/2.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexNews/4.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexCatalog/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexMarket/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexVertis/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexForDomain/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; MirrorDetector; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexSpravBot/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexSearchShop/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 "
    "(compatible; YandexMedianaBot/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexOntoDB/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexOntoDBAPI/1.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; YandexVerticals/1.0; +http://yandex.com/bots)",
]

MAIL_RU = [
    "Mozilla/5.0 (compatible; Mail.RU_Bot/Fast/2.0)",
]

RAMBLER = [
    "StackRambler/2.0 (MSIE incompatible)",
    "StackRambler/2.0",
]

YAHOO = [
    "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    "Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)",
]

MSN = [
    "msnbot/1.1 (+http://search.msn.com/msnbot.htm)",
    "msnbot-media/1.0 (+http://search.msn.com/msnbot.htm)",
    "msnbot-media/1.1 (+http://search.msn.com/msnbot.htm)",
    "msnbot-news (+http://search.msn.com/msnbot.htm)",
]

BING = [
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
]

ALL = []
ALL.extend(GOOGLE)
ALL.extend(YANDEX)
ALL.extend(MAIL_RU)
ALL.extend(RAMBLER)
ALL.extend(YAHOO)
ALL.extend(MSN)
ALL.extend(BING)


if __name__ == "__main__":
    import random
    print(random.choice(ALL))
