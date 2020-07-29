#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
from dataclasses import dataclass, field
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from typing import List, Union
import traceback
import re
import sys

from bs4 import BeautifulSoup, Tag

sys.path.append('..')
from shorten import shorten


URL_BASE = 'https://bash.im'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'


@dataclass
class Quote:
    url: str
    text: str
    date: DT.date
    rating: int
    comics_url: List[str] = field(default_factory=list)

    @property
    def id(self) -> int:
        return self._id

    @property
    def date_str(self) -> str:
        return self._date_str

    def __post_init__(self):
        self._id = int(self.url.rstrip().split('/')[-1])
        self._date_str = self.date.strftime('%d.%m.%Y')

    @staticmethod
    def parse_from(url_or_el: Union[str, Tag]) -> 'Quote':
        if isinstance(url_or_el, str):
            url = url_or_el

            with urlopen(Request(url, headers={'User-Agent': USER_AGENT})) as f:
                root = BeautifulSoup(f.read(), 'html.parser')
                quote_el = root.select_one('article.quote')
        else:
            quote_el = url_or_el

        comics_url = []
        strips_el = quote_el.select_one('.quote__strips')
        if strips_el:
            comics_url += [
                urljoin(URL_BASE, a['href']) for a in strips_el.select('.quote__strips_link')
            ]

            # Удаление тега, чтобы при получении текста цитаты не было в нем лишний текст
            strips_el.decompose()

        href = quote_el.select_one('.quote__header_permalink')['href']
        url = urljoin(URL_BASE, href)

        quote_text = quote_el.select_one('.quote__body').get_text(separator='\n', strip=True)
        rating = int(quote_el.select_one('.quote__total').get_text())

        # Example: 07.12.2011 в 11:11
        m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', quote_el.select_one('.quote__header_date').get_text())
        day, month, year = map(int, m.groups())
        date = DT.date(year, month, day)

        return Quote(url, quote_text, date, rating, comics_url)

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, url={self.url}, ' \
               f'text({len(self.text)})={shorten(self.text)!r}, ' \
               f'date={self.date_str}, rating={self.rating}, comics_url={self.comics_url})'


def get_random_quotes_list() -> List[Quote]:
    url = 'https://bash.im/random'
    quotes = []

    try:
        with urlopen(Request(url, headers={'User-Agent': USER_AGENT})) as f:
            root = BeautifulSoup(f.read(), 'html.parser')

            for quote_el in root.select('article.quote.quote'):
                try:
                    quotes.append(
                        Quote.parse_from(quote_el)
                    )
                except Exception:
                    print(f'Error by parsing quote:\n\n{traceback.format_exc()}\n\nquote_el:\n{quote_el}')

    except Exception:
        print(traceback.format_exc())

    return quotes


if __name__ == '__main__':
    print(Quote.parse_from('https://bash.im/quote/414617'))
    # Quote(id=414617, url=https://bash.im/quote/414617, text(96)='zvizda: диета достигла той упо...', date=07.12.2011, rating=11843, comics_url=['https://bash.im/strip/20190828', 'https://bash.im/strip/20200408'])

    print(Quote.parse_from('https://bash.im/quote/454588'))
    # Quote(id=454588, url=https://bash.im/quote/454588, text(97)='- К человеку с ножом обращаютс...', date=20.02.2019, rating=1351, comics_url=[])

    print(Quote.parse_from('https://bash.im/quote/443711'))
    # Quote(id=443711, url=https://bash.im/quote/443711, text(402)='Звонит щас абонент, говорит ин...', date=28.02.2017, rating=5410, comics_url=[])

    print()

    quotes = get_random_quotes_list()
    print(f'Quotes({len(quotes)}):')
    for i, quote in enumerate(quotes, 1):
        print(f'  {i:2}. {quote}')

    # Quotes(25):
    #    1. Quote(id=405265, url=https://bash.im/quote/405265, text(182)='С форума об автоматизации рабо...', date=08.12.2009, rating=7305, comics_url=[])
    #    2. Quote(id=456451, url=https://bash.im/quote/456451, text(148)='xxx: Это всеравно что говорить...', date=25.06.2019, rating=1012, comics_url=[])
    #    3. Quote(id=260746, url=https://bash.im/quote/260746, text(131)='Lina: ПАМАГИТЕ!!! Целый весь о...', date=31.05.2007, rating=5561, comics_url=[])
    #    4. Quote(id=402098, url=https://bash.im/quote/402098, text(200)='st41ker: привет, как оно ничег...', date=12.01.2009, rating=11063, comics_url=[])
    #    5. Quote(id=278834, url=https://bash.im/quote/278834, text(317)='xxxx:\nСегодня был у друзей мам...', date=04.06.2007, rating=2572, comics_url=[])
    #    6. Quote(id=457518, url=https://bash.im/quote/457518, text(154)='SFM: сегодня почуствовал себя ...', date=01.09.2019, rating=2125, comics_url=[])
    #    7. Quote(id=43390, url=https://bash.im/quote/43390, text(155)='<Мал> установи лимит на количе...', date=21.08.2006, rating=2931, comics_url=[])
    #    8. Quote(id=436563, url=https://bash.im/quote/436563, text(187)='- Я не понимаю, почему, когда ...', date=11.11.2015, rating=4922, comics_url=[])
    #    9. Quote(id=440164, url=https://bash.im/quote/440164, text(186)='Al Dragon:\nКое-что о FAST, Fiv...', date=11.07.2016, rating=1434, comics_url=[])
    #   10. Quote(id=411583, url=https://bash.im/quote/411583, text(97)='xxx: мне сказали, что я очень ...', date=07.06.2011, rating=7076, comics_url=[])
    #   11. Quote(id=421264, url=https://bash.im/quote/421264, text(164)='Янyлькa: снова не могу фотку д...', date=18.02.2013, rating=4481, comics_url=[])
    #   12. Quote(id=405810, url=https://bash.im/quote/405810, text(580)='Sklep - ночевали с друзьями у ...', date=11.02.2010, rating=14084, comics_url=[])
    #   13. Quote(id=452822, url=https://bash.im/quote/452822, text(249)='В Шоколаднице сейчас новое мен...', date=22.10.2018, rating=1709, comics_url=[])
    #   14. Quote(id=14153, url=https://bash.im/quote/14153, text(179)='Парень>> ;)\nДевушка>> здравств...', date=15.03.2006, rating=4532, comics_url=[])
    #   15. Quote(id=403708, url=https://bash.im/quote/403708, text(328)='Неми:\nБабушкиной сестре купили...', date=22.06.2009, rating=14884, comics_url=[])
    #   16. Quote(id=455229, url=https://bash.im/quote/455229, text(147)='xxx: Услышав мамино «была крас...', date=02.04.2019, rating=2065, comics_url=[])
    #   17. Quote(id=440899, url=https://bash.im/quote/440899, text(280)='X: Три недели тестирую большой...', date=26.08.2016, rating=959, comics_url=[])
    #   18. Quote(id=414336, url=https://bash.im/quote/414336, text(141)='@e_vilelf: при выставлении оце...', date=20.11.2011, rating=10234, comics_url=[])
    #   19. Quote(id=407209, url=https://bash.im/quote/407209, text(97)='-Ты температуру мерял?\n-Нет ещ...', date=05.07.2010, rating=2125, comics_url=[])
    #   20. Quote(id=425690, url=https://bash.im/quote/425690, text(209)='seberya: Да ты выложи на ютуб ...', date=02.12.2013, rating=6228, comics_url=[])
    #   21. Quote(id=392769, url=https://bash.im/quote/392769, text(212)='H@Lee\nЯ короче сжал между зубо...', date=24.10.2007, rating=3701, comics_url=[])
    #   22. Quote(id=413492, url=https://bash.im/quote/413492, text(79)='Из описания заявки на ремонт:\n...', date=28.09.2011, rating=9019, comics_url=[])
    #   23. Quote(id=391228, url=https://bash.im/quote/391228, text(322)='un1ck: Сегодня у нас в городе ...', date=06.08.2007, rating=7112, comics_url=[])
    #   24. Quote(id=428827, url=https://bash.im/quote/428827, text(161)='xxx:\nВечер, под окном шумят а ...', date=27.06.2014, rating=2447, comics_url=[])
    #   25. Quote(id=402706, url=https://bash.im/quote/402706, text(63)='Donn: настоящих геймеров в арм...', date=02.03.2009, rating=3532, comics_url=[])
