#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.parse import unquote

# pip install pymediawiki
# https://github.com/barrust/mediawiki
# http://pymediawiki.readthedocs.io/en/latest/index.html
from mediawiki import MediaWiki


def wiki_search(query: str, lang="ru", unquote_percent_encoded=False) -> str:
    # Default using wikipedia
    wikipedia = MediaWiki(lang=lang)
    result = wikipedia.opensearch(query, results=1)
    if not result:
        return ""

    _, text, url = result[0]

    if unquote_percent_encoded:
        url = unquote(url)

    return "{} ({})".format(text, url)


if __name__ == "__main__":
    query = "GitHub"
    print(wiki_search(query))

    query = "python"
    print(wiki_search(query))

    query = "магнитогорск"
    print(wiki_search(query))
    print(wiki_search(query, unquote_percent_encoded=True))
