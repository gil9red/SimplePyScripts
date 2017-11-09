#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def wiki_search(query: str, lang='ru') -> str:
    # pip install pymediawiki
    # Default using wikipedia
    from mediawiki import MediaWiki
    wikipedia = MediaWiki(lang=lang)
    result = wikipedia.opensearch(query, results=1)
    if not result:
        return ''

    _, text, url = result[0]
    return '{} ({})'.format(text, url)


if __name__ == '__main__':
    query = 'GitHub'
    print(wiki_search(query))

    query = 'python'
    print(wiki_search(query))

    query = 'магнитогорск'
    print(wiki_search(query))
