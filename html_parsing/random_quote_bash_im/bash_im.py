#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
from dataclasses import dataclass, field
from urllib.parse import urljoin
from typing import List, Union
import traceback
from pathlib import Path
import re

from bs4 import BeautifulSoup, Tag
import requests


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/9c9a5555e87d7a7475c2dc8feffb97f2906789ce/shorten.py#L7
def shorten(text: str, length=30) -> str:
    if len(text) > length:
        text = text[:length] + '...'
    return text


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

    def download_comics(self, dir_name: Union[str, Path] = None, logger=None) -> List[str]:
        if isinstance(dir_name, str):
            dir_name = Path(dir_name)

        if dir_name is None:
            dir_name = Path(f'comics/quote_{self.id}')

        files = []

        for url in self.comics_url:
            try:
                dir_name.mkdir(parents=True, exist_ok=True)

                comics_id = url.rstrip('/').split('/')[-1]
                file_name = dir_name / f'{comics_id}.png'

                # Если нет файла, скачиваем
                if not file_name.exists():
                    session = requests.session()
                    session.headers['User-Agent'] = USER_AGENT

                    # Страница комикса
                    rs = session.get(url)
                    root = BeautifulSoup(rs.content, 'html.parser')

                    img_el = root.select_one('.quote__img')
                    url_src = img_el.get('src') or img_el.get('data-src')
                    url_img = urljoin(URL_BASE, url_src)

                    # Картинка комикса
                    rs = session.get(url_img)
                    file_name.write_bytes(rs.content)

                files.append(str(file_name.resolve()))

            except Exception:
                msg = f'Error by parsing comics {url}:\n\n'
                if logger:
                    logger.exception(msg)
                else:
                    print(f'{msg}{traceback.format_exc()}')

        return files

    @staticmethod
    def parse_from(url_or_el: Union[str, Tag]) -> 'Quote':
        if isinstance(url_or_el, str):
            url = url_or_el

            rs = requests.get(url, headers={'User-Agent': USER_AGENT})
            root = BeautifulSoup(rs.content, 'html.parser')
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

        # У некоторых цитат не указан рейтинг, выглядит как: ...
        # Например, в https://bash.im/quote/416789
        try:
            rating = int(quote_el.select_one('.quote__total').get_text())
        except:
            rating = 0

        # Example: "07.12.2011 в 11:11"
        m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', quote_el.select_one('.quote__header_date').get_text())
        day, month, year = map(int, m.groups())
        date = DT.date(year, month, day)

        return Quote(url, quote_text, date, rating, comics_url)

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, url={self.url}, ' \
               f'text({len(self.text)})={shorten(self.text)!r}, ' \
               f'date={self.date_str}, rating={self.rating}, comics_url={self.comics_url})'


def get_random_quotes_list(logger=None) -> List[Quote]:
    url = 'https://bash.im/random'
    quotes = []

    try:
        rs = requests.get(url, headers={'User-Agent': USER_AGENT})
        root = BeautifulSoup(rs.content, 'html.parser')

        for quote_el in root.select('article.quote'):
            try:
                quotes.append(
                    Quote.parse_from(quote_el)
                )
            except Exception:
                msg = f'Error by parsing quote:\nquote_el:\n{quote_el}\n\n'
                if logger:
                    logger.exception(msg)
                else:
                    print(f'{msg}{traceback.format_exc()}')

    except Exception:
        if logger:
            logger.exception('')
        else:
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
    #   1. Quote(id=402770, url=https://bash.im/quote/402770, text(224)='Владивосток. Январь.\nНочь посл...', date=08.03.2009, rating=26693, comics_url=[])
    #   2. Quote(id=411254, url=https://bash.im/quote/411254, text(159)='marikus: :(...\nazon: чё рожа к...', date=23.05.2011, rating=8145, comics_url=[])
    #   3. Quote(id=439536, url=https://bash.im/quote/439536, text(179)='<Faumi> Guest42, мне как-то ка...', date=31.05.2016, rating=3950, comics_url=[])
    #   4. Quote(id=395616, url=https://bash.im/quote/395616, text(75)='xxx: Здесь кто-нибудь есть?\nyy...', date=18.03.2008, rating=6421, comics_url=[])
    #   5. Quote(id=461326, url=https://bash.im/quote/461326, text(148)='xxx: я в этом вашем футболе не...', date=22.05.2020, rating=3638, comics_url=[])
    #   6. Quote(id=400421, url=https://bash.im/quote/400421, text(218)='Египет, Дахаб, отель Тропитель...', date=22.10.2008, rating=33192, comics_url=[])
    #   7. Quote(id=177929, url=https://bash.im/quote/177929, text(456)='takopus:\nВирус вирусу рознь, к...', date=18.04.2007, rating=5687, comics_url=[])
    #   8. Quote(id=394244, url=https://bash.im/quote/394244, text(35)='irc:\n<Klimax> Девчата а вот и ...', date=15.01.2008, rating=4578, comics_url=[])
    #   9. Quote(id=159922, url=https://bash.im/quote/159922, text(172)='LJ\nasper> Кстати, гель для ана...', date=05.04.2007, rating=9014, comics_url=[])
    #  10. Quote(id=385961, url=https://bash.im/quote/385961, text(251)='После обмена фотами:\nОн: А ты ...', date=05.07.2007, rating=6522, comics_url=[])
    #  11. Quote(id=391805, url=https://bash.im/quote/391805, text(761)='PostGoblin: Реальная стори: го...', date=05.09.2007, rating=19314, comics_url=[])
    #  12. Quote(id=457812, url=https://bash.im/quote/457812, text(325)='Еду из деревни, воскресенье, в...', date=19.09.2019, rating=1362, comics_url=[])
    #  13. Quote(id=432316, url=https://bash.im/quote/432316, text(251)='den_stranger: В коридоре нашег...', date=10.02.2015, rating=5836, comics_url=[])
    #  14. Quote(id=9246, url=https://bash.im/quote/9246, text(331)='DX: Слушай сайт сломал А потри...', date=27.01.2006, rating=1286, comics_url=[])
    #  15. Quote(id=441685, url=https://bash.im/quote/441685, text(388)='xxx: я сусликов на Татышева ко...', date=15.10.2016, rating=5793, comics_url=[])
    #  16. Quote(id=401093, url=https://bash.im/quote/401093, text(363)='Urko: Ты написал объявление в ...', date=18.11.2008, rating=13327, comics_url=[])
    #  17. Quote(id=429674, url=https://bash.im/quote/429674, text(550)='Вы, любители завоеваний и даль...', date=20.08.2014, rating=4516, comics_url=[])
    #  18. Quote(id=443083, url=https://bash.im/quote/443083, text(677)='С гиктаймс:\nBrenwen: Такое чув...', date=17.01.2017, rating=2281, comics_url=[])
    #  19. Quote(id=454087, url=https://bash.im/quote/454087, text(61)='XXX: Макароны по-флотски - это...', date=18.01.2019, rating=1784, comics_url=[])
    #  20. Quote(id=91035, url=https://bash.im/quote/91035, text(167)='[**ИгнааааТ**]\nа просто тупо b...', date=17.01.2007, rating=3860, comics_url=[])
    #  21. Quote(id=429826, url=https://bash.im/quote/429826, text(486)='<Unicornix> а знаете ли вы, чт...', date=29.08.2014, rating=3550, comics_url=[])
    #  22. Quote(id=397851, url=https://bash.im/quote/397851, text(193)='~lotos~:Ржунимагу, стою в мага...', date=15.07.2008, rating=21320, comics_url=['https://bash.im/strip/20081022'])
    #  23. Quote(id=217468, url=https://bash.im/quote/217468, text(687)='*****:\nНастроил в квартире сет...', date=13.05.2007, rating=5847, comics_url=[])
    #  24. Quote(id=404924, url=https://bash.im/quote/404924, text(279)='Воланд: Дорогая Лиза, я понима...', date=30.10.2009, rating=8788, comics_url=[])
    #  25. Quote(id=417637, url=https://bash.im/quote/417637, text(166)='xxx: Блин. Нормальные люди, ко...', date=26.06.2012, rating=7810, comics_url=[])

    print()

    quote = Quote.parse_from('https://bash.im/quote/414617')
    files = quote.download_comics()
    print(f'Files ({len(files)}):')
    for i, file_name in enumerate(files, 1):
        print(f'  {i:2}. {file_name}')
