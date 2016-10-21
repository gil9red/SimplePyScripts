#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# http://www.cbr.ru/scripts/XML_daily.asp
# http://www.cbr.ru/scripts/XML_daily.asp?date_req=21.10.2016

if __name__ == '__main__':
    # from datetime import date
    # date_req = date.today().strftime('%d.%m.%Y')
    # url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + date_req
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'

    from urllib.request import urlopen
    with urlopen(url) as f:
        from lxml import etree
        root = etree.XML(f.read())

        # 840 / 978
        # <ValCurs Date="21.10.2016" name="Foreign Currency Market">
        #     <Valute ID="R01010">
        #         <NumCode>036</NumCode>
        #         <CharCode>AUD</CharCode>
        #         <Nominal>1</Nominal>
        #         <Name>Австралийский доллар</Name>
        #         <Value>47,8382</Value>
        #     </Valute>
        print(root.attrib['Date'])
        for valute in root:
            currency = valute.xpath('child::CharCode/text()')[0]
            value = valute.xpath('child::Value/text()')[0]
            print(currency)
            if currency in ['840', '978']:
                print(currency, value)
