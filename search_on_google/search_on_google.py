__author__ = "ipetrash"


"""Пример поиска по гуглу."""


if __name__ == "__main__":
    from urllib.parse import quote_plus
    from grab import Grab

    url_pattern = "https://www.google.ru/search?q="
    search_text = "манга читать онлайн"

    url = url_pattern + quote_plus(search_text)

    g = Grab()
    g.go(url)

    print(g.response.url)

    print(g.doc.select('//div[@id="resultStats"]').text())

    search_result = g.doc.select('//li[@class="g"]/*/h3/a')
    for i, c in enumerate(search_result, 1):
        print(f'{i}. "{c.text()}": {c.attr("href")}')
