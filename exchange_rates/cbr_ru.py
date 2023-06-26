#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import date
from urllib.request import urlopen

from lxml import etree


def exchange_rate(currency, date_req=None):
    """Return exchange rate currency for rub.

    currency: alpha3code, example "USD"
    date_req: date, example 21.10.2016

    """

    # Example:
    # http://www.cbr.ru/scripts/XML_daily.asp
    # http://www.cbr.ru/scripts/XML_daily.asp?date_req=21.10.2016
    if date_req is None:
        date_req = date.today()

    if isinstance(date_req, date):
        date_req = date_req.strftime("%d.%m.%Y")

    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date_req
    # url = 'http://www.cbr.ru/scripts/XML_daily.asp'

    with urlopen(url) as f:
        root = etree.XML(f.read())

        # <ValCurs Date="21.10.2016" name="Foreign Currency Market">
        #     <Valute ID="R01010">
        #         <NumCode>036</NumCode>
        #         <CharCode>AUD</CharCode>
        #         <Nominal>1</Nominal>
        #         <Name>Австралийский доллар</Name>
        #         <Value>47,8382</Value>
        #     </Valute>
        #     ...

        for valute in root:
            ccy = valute.xpath("child::CharCode/text()")[0]
            value = valute.xpath("child::Value/text()")[0]

            if currency == ccy:
                return float(value.replace(",", ".")), root.attrib["Date"]

    return None, None


if __name__ == "__main__":
    print("USD:", exchange_rate("USD"))
    print("EUR:", exchange_rate("EUR"))

    from datetime import date, timedelta

    date_req = date.today()
    value, rate_date = exchange_rate("USD", date_req)
    print(f"{rate_date}: USD: {value}")

    date_req = date.today() - timedelta(days=1)
    value, rate_date = exchange_rate("USD", date_req)
    print(f"{rate_date}: USD: {value}")

    date_req = date.today() + timedelta(days=1)
    value, rate_date = exchange_rate("USD", date_req)
    print(f"{rate_date}: USD: {value}")

    date_req = date.today() + timedelta(days=2)
    value, rate_date = exchange_rate("USD", date_req)
    print(f"{rate_date}: USD: {value}")
