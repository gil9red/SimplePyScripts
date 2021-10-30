#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from typing import List, Tuple, Union

import requests
from bs4 import BeautifulSoup, Tag


PATTERN_GET_NUMBER_OF_STEVES = re.compile(r'(\d+) Steves have signed the statement', flags=re.IGNORECASE)
PATTERN_MANY_NEWLINES = re.compile(r'\n{2,}')
PATTERN_MANY_EMPTY = re.compile(r'\s{2,}')

session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'

URL = 'https://ncse.ngo/list-steves'


def get_number_from_description() -> int:
    rs = session.get(URL)
    m = PATTERN_GET_NUMBER_OF_STEVES.search(rs.text)
    if not m:
        raise Exception('Not found number of Steves!')

    return int(m.group(1))


def _get_stripped_text(text: str) -> str:
    if not text:
        return text

    text = PATTERN_MANY_NEWLINES.sub('\n', text)
    text = PATTERN_MANY_EMPTY.sub(' ', text)
    return text.strip()


def _get_text(el: Union[Tag, str]) -> str:
    return _get_stripped_text(el) if isinstance(el, str) else _get_stripped_text(el.text)


def _remove_postfix(text: str) -> str:
    return text.replace('*', '').replace('†', '').strip()


def get_Steves() -> List[Tuple[str, str]]:
    items = []

    rs = session.get(URL)
    root = BeautifulSoup(rs.content, 'html.parser')

    p_items = root.select('.field-field_body > article > p:has(:is(strong, b))')

    for p in p_items:
        # Ignore <p> with footnotes
        if 'Added after the Project Steve 200 t-shirt was designed' in p.text:
            continue

        tag_name = p.strong or p.b
        if not tag_name:
            raise Exception('Could not find b / strong tag containing name!')

        name = _get_stripped_text(tag_name.text)
        name = _remove_postfix(name)

        # To prevent the name from being included in the description
        tag_name.decompose()
        description = _get_stripped_text(p.text)
        description = _remove_postfix(description)

        items.append((name, description))

    return items


if __name__ == '__main__':
    number = get_number_from_description()
    print(f'Number from description: {number}')
    # Number from description: 1472

    items = get_Steves()
    print(f'Total: {len(items)}')
    # Total: 1466

    print(f'''
First:
{items[0][0]}
{items[0][1]}

Last:
{items[-1][0]}
{items[-1][1]}
''')
    """
    First:
    Stephen T. Abedon
    Associate Professor of Microbiology, Ohio State University
    Ph.D., Microbiology, University of Arizona
    Creator of The Bacteriophage Ecology Group, Home of Phage Ecology and Evolutionary Biology (www.phage.org)
    
    Last:
    Steven W. Zucker
    David and Lucile Packard Professor of Computer Science and Biomedical Engineering and Director of the Yale Program in Applied Mathematics, Yale University
    Ph.D., Biomedical Engineering, Drexel University
    """
