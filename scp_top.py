#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# <span class="rateup
#
# рейтинг:
# <span class="number prw54353">+20</span>
# </span>
#
#
# <a id="pagerate-button" class="btn btn-default" href="javascript:;">
# Оценить (
# <span id="prw54355">-7</span>
# )
# </a>
#
# http://scpfoundation.ru/scp-009


from grab import Grab


url = "http://scpfoundation.ru/scp-"

g = Grab()

scp_rate_list = list()

for i in range(100):
    scp_url = url + str(i).rjust(3, "0")

    g.go(scp_url)

    try:
        result = g.doc.select('//span[contains(@class, "prw54353")]')
        if result.count() == 0:
            result = g.doc.select('//span[@id="prw54355"]')

        rate = int(result.text())
    except Exception as e:
        print(scp_url, e)
        continue

    scp_rate_list.append((scp_url, rate))

print()
print()
for url, rate in sorted(scp_rate_list, reverse=True, key=lambda x: x[1])[:10]:
    print(url, rate)
