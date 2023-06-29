#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import traceback
import re
import shutil

from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin
from typing import List, Union, Optional

import requests
from bs4 import BeautifulSoup, Tag


def parse(obj) -> BeautifulSoup:
    return BeautifulSoup(obj, "html.parser")


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/cd5bf42742b2de4706a82aecb00e20ca0f043f8e/shorten.py#L7
def shorten(text: str, length=30) -> str:
    if not text:
        return text

    if len(text) > length:
        text = text[:length] + "..."
    return text


def get_plaintext(element: Tag) -> str:
    items = []
    for elem in element.descendants:
        if isinstance(elem, str):
            items.append(elem.strip())
        elif elem.name in ["br", "p"]:
            items.append("\n")
    return "".join(items).strip()


DIR = Path(__file__).resolve().parent

DATE_FORMAT_QUOTE = "%d.%m.%Y"

URL_BASE = "https://bash.im"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
)

session = requests.session()
session.headers["User-Agent"] = USER_AGENT


@dataclass
class Quote:
    url: str
    text: str
    date: dt.date
    rating: int
    comics_urls: List[str] = field(default_factory=list)

    @property
    def id(self) -> int:
        return self._id

    @property
    def date_str(self) -> str:
        return self._date_str

    def __post_init__(self):
        self._id = int(self.url.rstrip().split("/")[-1])
        self._date_str = self.date.strftime(DATE_FORMAT_QUOTE)

    def download_comics(
        self, dir_name: Union[str, Path] = None, logger=None
    ) -> List[str]:
        if isinstance(dir_name, str):
            dir_name = Path(dir_name)

        if dir_name is None:
            dir_name = DIR / "comics"

        files = []

        for url in self.comics_urls:
            try:
                dir_name.mkdir(parents=True, exist_ok=True)

                comics_id = url.rstrip("/").split("/")[-1]
                file_name = dir_name / f"quote{self.id}_{comics_id}.png"

                # Если нет файла, скачиваем
                if not file_name.exists():
                    # Страница комикса
                    rs = session.get(url)
                    rs.raise_for_status()
                    root = parse(rs.content)

                    img_el = root.select_one(".quote__img")
                    url_src = img_el.get("src") or img_el.get("data-src")
                    url_img = urljoin(URL_BASE, url_src)

                    # Картинка комикса
                    rs = session.get(url_img)
                    rs.raise_for_status()
                    file_name.write_bytes(rs.content)

                files.append(str(file_name.resolve()))

            except Exception:
                msg = f"Error by parsing comics {url}:\n\n"
                if logger:
                    logger.exception(msg)
                else:
                    print(f"{msg}{traceback.format_exc()}")

        return files

    @staticmethod
    def parse_from(url__id__el: Union[str, int, Tag]) -> Optional["Quote"]:
        if isinstance(url__id__el, int):
            url__id__el = f"{URL_BASE}/quote/{url__id__el}"

        if isinstance(url__id__el, str):
            url = url__id__el

            rs = session.get(url)
            rs.raise_for_status()

            # Если был редирект на главную страницу, значит нет цитаты с указанным id
            if rs.url.rstrip("/") == URL_BASE:
                return

            root = parse(rs.content)
            quote_el = root.select_one("article.quote")

        else:
            quote_el = url__id__el

        comics_urls = []
        strips_el = quote_el.select_one(".quote__strips")
        if strips_el:
            comics_urls += [
                urljoin(URL_BASE, a["href"])
                for a in strips_el.select(".quote__strips_link")
            ]

            # Удаление тега, чтобы при получении текста цитаты не было в нем лишний текст
            strips_el.decompose()

        href = quote_el.select_one(".quote__header_permalink")["href"]
        url = urljoin(URL_BASE, href)

        quote_text = get_plaintext(quote_el.select_one(".quote__body"))

        # У некоторых цитат не указан рейтинг, выглядит как: ...
        # Например, в https://bash.im/quote/416789
        try:
            rating = int(quote_el.select_one(".quote__total").get_text())
        except:
            rating = 0

        # Example: "07.12.2011 в 11:11"
        m = re.search(
            r"(\d{2})\.(\d{2})\.(\d{4})",
            quote_el.select_one(".quote__header_date").get_text(),
        )
        day, month, year = map(int, m.groups())
        date = dt.date(year, month, day)

        return Quote(url, quote_text, date, rating, comics_urls)

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, url={self.url}, "
            f"text({len(self.text)})={shorten(self.text)!r}, "
            f"date={self.date_str}, rating={self.rating}, comics_urls={self.comics_urls})"
        )


def get_random_quotes(logger=None) -> List[Quote]:
    url = f"{URL_BASE}/random"
    quotes = []

    try:
        rs = session.get(url)
        rs.raise_for_status()
        root = parse(rs.content)

        for quote_el in root.select("article.quote"):
            try:
                quotes.append(Quote.parse_from(quote_el))
            except Exception:
                msg = f"Error by parsing quote:\nquote_el:\n{quote_el}\n\n"
                if logger:
                    logger.exception(msg)
                else:
                    print(f"{msg}{traceback.format_exc()}")

    except Exception:
        if logger:
            logger.exception("")
        else:
            print(traceback.format_exc())

    return quotes


def get_page_quotes(page=None, logger=None) -> List[Quote]:
    url = URL_BASE
    if page:
        url = urljoin(url, f"/index/{page}")

    quotes = []

    try:
        rs = session.get(url)
        rs.raise_for_status()
        root = parse(rs.content)

        for quote_el in root.select("article.quote"):
            try:
                quotes.append(Quote.parse_from(quote_el))
            except Exception:
                msg = f"Error by parsing quote:\nquote_el:\n{quote_el}\n\n"
                if logger:
                    logger.exception(msg)
                else:
                    print(f"{msg}{traceback.format_exc()}")

    except Exception:
        if logger:
            logger.exception("")
        else:
            print(traceback.format_exc())

    return quotes


def get_main_page_quotes(logger=None) -> List[Quote]:
    return get_page_quotes(logger=logger)


def get_total_pages() -> int:
    rs = session.get(URL_BASE)
    rs.raise_for_status()
    root = parse(rs.content)

    return int(root.select_one(".pager__input")["max"])


def parser_health_check(raise_error=False) -> Optional[str]:
    """
    Функция проверяет работу парсера.
    Если функция вернет None, значит проблем нет, иначе вернется строка с описанием проблемы.
    """

    def _test_quote(quote: Quote, expected_id: int):
        assert quote, f"Цитата с #{expected_id} должна существовать!"
        assert (
            quote.id == expected_id
        ), f"Id цитаты #{quote.id} не совпадает с ожидаемым #{expected_id}!"

        assert quote.url, f"Поле url цитаты #{expected_id} должно быть заполнено!"
        assert isinstance(
            quote.url, str
        ), f"Поле url цитаты #{expected_id} должно иметь тип str!"

        assert quote.text, f"Поле text цитаты #{expected_id} должно быть заполнено!"
        assert isinstance(
            quote.text, str
        ), f"Поле text цитаты #{expected_id} должно иметь тип str!"

        assert quote.date, f"Поле date цитаты #{expected_id} должно быть заполнено!"
        assert isinstance(
            quote.date, dt.date
        ), f"Поле date цитаты #{expected_id} должно иметь тип date!"

        assert quote.rating, f"Поле rating цитаты #{expected_id} должно быть заполнено!"
        assert isinstance(
            quote.rating, int
        ), f"Поле rating цитаты #{expected_id} должно иметь тип int!"

        assert (
            quote.comics_urls
        ), f"Поле comics_urls цитаты #{expected_id} должно быть заполнено!"

        # Скачаем комиксы
        dir_comics = DIR / "_test__comics"
        files = quote.download_comics(dir_comics)

        assert files, f"Не найдены файлы комиксов цитаты #{expected_id}!"
        assert len(files) == len(quote.comics_urls), (
            f"Количество файлов комиксов (={len(files)}) не совпадает с количеством ссылок "
            f"на комиксы (={len(quote.comics_urls)}) в цитате #{expected_id}!"
        )

        # Проверим размеры файлов комиксов
        for file in files:
            file_size = Path(file).stat().st_size
            assert (
                file_size > 0
            ), f"Файл комикса {file!r} в цитате #{expected_id} пустой!"

        # Удаляем папку комиксов
        shutil.rmtree(dir_comics)

    try:
        # Цитата с комиксами
        quote_id = 414617

        quote = Quote.parse_from(quote_id)
        _test_quote(quote, quote_id)

        quote = Quote.parse_from(f"https://bash.im/quote/{quote_id}")
        _test_quote(quote, quote_id)

    except requests.exceptions.HTTPError as e:
        if raise_error:
            raise e
        return f"Сетевая проблема: {str(e)!r}"

    except AssertionError as e:
        if raise_error:
            raise e
        return f"Обнаружена проблема: {str(e)!r}"

    except Exception as e:
        if raise_error:
            raise e
        return f"Неизвестная проблема: {str(e)!r}"


if __name__ == "__main__":
    error_text = parser_health_check()
    assert not error_text, f"Обнаружена проблема: {error_text!r}"

    total_pages = get_total_pages()
    print("Total pages:", total_pages)
    print()

    print(Quote.parse_from("https://bash.im/quote/414617"))
    # Quote(id=414617, url=https://bash.im/quote/414617, text(96)='zvizda: диета достигла той упо...', date=07.12.2011, rating=11843, comics_urls=['https://bash.im/strip/20190828', 'https://bash.im/strip/20200408'])

    print(Quote.parse_from(414617))
    # Quote(id=414617, url=https://bash.im/quote/414617, text(96)='zvizda: диета достигла той упо...', date=07.12.2011, rating=11849, comics_urls=['https://bash.im/strip/20190828', 'https://bash.im/strip/20200408'])

    print(Quote.parse_from("https://bash.im/quote/454588"))
    # Quote(id=454588, url=https://bash.im/quote/454588, text(97)='- К человеку с ножом обращаютс...', date=20.02.2019, rating=1351, comics_urls=[])

    print(Quote.parse_from("https://bash.im/quote/443711"))
    # Quote(id=443711, url=https://bash.im/quote/443711, text(402)='Звонит щас абонент, говорит ин...', date=28.02.2017, rating=5410, comics_urls=[])

    print()

    quotes = get_random_quotes()
    print(f"Random quotes ({len(quotes)}):")

    for i, quote in enumerate(quotes, 1):
        print(f"  {i:2}. {quote}")
        # print(quote.text)
        # print('\n' + '-' * 100 + '\n')
    """
    Quotes(25):
      1. Quote(id=402770, url=https://bash.im/quote/402770, text(224)='Владивосток. Январь.\nНочь посл...', date=08.03.2009, rating=26693, comics_urls=[])
      2. Quote(id=411254, url=https://bash.im/quote/411254, text(159)='marikus: :(...\nazon: чё рожа к...', date=23.05.2011, rating=8145, comics_urls=[])
      3. Quote(id=439536, url=https://bash.im/quote/439536, text(179)='<Faumi> Guest42, мне как-то ка...', date=31.05.2016, rating=3950, comics_urls=[])
      ...
     22. Quote(id=397851, url=https://bash.im/quote/397851, text(193)='~lotos~:Ржунимагу, стою в мага...', date=15.07.2008, rating=21320, comics_urls=['https://bash.im/strip/20081022'])
     23. Quote(id=217468, url=https://bash.im/quote/217468, text(687)='*****:\nНастроил в квартире сет...', date=13.05.2007, rating=5847, comics_urls=[])
     24. Quote(id=404924, url=https://bash.im/quote/404924, text(279)='Воланд: Дорогая Лиза, я понима...', date=30.10.2009, rating=8788, comics_urls=[])
     25. Quote(id=417637, url=https://bash.im/quote/417637, text(166)='xxx: Блин. Нормальные люди, ко...', date=26.06.2012, rating=7810, comics_urls=[])
    """
    print()

    quotes_main = get_main_page_quotes()
    print(
        f"Main page quotes ({len(quotes_main)}), first #{quotes_main[0].id}, last #{quotes_main[-1].id}"
    )

    quotes_first_page = get_page_quotes(page=total_pages)
    print(
        f"Main page quotes v2 ({len(quotes_first_page)}), first #{quotes_first_page[0].id}, last #{quotes_first_page[-1].id}"
    )
    assert quotes_main[0].id == quotes_first_page[0].id
    assert quotes_main[-1].id == quotes_first_page[-1].id

    page = 100
    quotes = get_page_quotes(page=page)
    print(
        f"Quotes from {page} page: ({len(quotes)}), first #{quotes[0].id}, last #{quotes[-1].id}"
    )
    print()

    quote = Quote.parse_from("https://bash.im/quote/414617")
    files = quote.download_comics()
    print(f"Files ({len(files)}):")
    for i, file_name in enumerate(files, 1):
        print(f"  {i:2}. {file_name}")

    root = parse("123<br>abc<p>HEX</p><br><br>!!!")
    text = get_plaintext(root)
    assert text == "123\nabc\nHEX\n\n!!!"

    assert Quote.parse_from(0) is None
