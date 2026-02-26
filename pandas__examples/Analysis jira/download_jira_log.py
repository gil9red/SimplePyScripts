#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pathlib

from datetime import datetime
from urllib.parse import urlparse

from bs4 import BeautifulSoup


URL = "https://helpdesk.compassluxe.com/sr/jira.issueviews:searchrequest-xml/24381/SearchRequest-24381.xml?tempMax=1000"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
}

# NOTE. Get <PEM_FILE_NAME>: openssl pkcs12 -nodes -out key.pem -in file.p12
PEM_FILE_NAME = "ipetrash.pem"

FILE_NAME = "jira_log__clear.xml"
FILE_NAME_FULL = "jira_log.xml"


def generate_file_name(url: str) -> str:
    """
    'https://jira.foobar.ru/sr/jira.issueviews:searchrequest-xml/24381/SearchRequest-24381.xml?tempMax=1000' ->
    'SearchRequest-24381.xml__tempMax=1000__2017-11-07.xml'

    :param url:
    :return:
    """

    result = urlparse(url)
    path = pathlib.Path(result.path)
    current_date_str = datetime.now().date().strftime("%Y-%m-%d")

    return f"{path.name}__{result.query}__{current_date_str}.xml"


def clear_jira_xml(xml_content: bytes) -> bytes:
    xml_content = (
        xml_content.replace(b"TranzAxis", b"FooBar")
        .replace(b"compassplus", b"foobar")
        .replace(b"Compass Plus", b"Foo Bar")
    )

    root = BeautifulSoup(xml_content, "html.parser")

    def mask_tag_content(css_selector, attr=None) -> None:
        for x in root.select(css_selector):
            x.string = "..."

            if attr:
                x[attr] = "..."

    def delete_tag(css_selector) -> None:
        for x in root.select(css_selector):
            x.decompose()

    delete_tag("comments > comment")
    delete_tag("attachments > attachment")
    delete_tag("customfields")
    delete_tag("issuelinks")
    delete_tag("subtasks")

    mask_tag_content("[username]", "username")
    mask_tag_content("item > title")
    mask_tag_content("item > summary")
    mask_tag_content("item > description")
    mask_tag_content("item > link")
    mask_tag_content("item > key")
    mask_tag_content("item > version")
    mask_tag_content("item > fixversion")
    mask_tag_content("item > component")
    mask_tag_content("item > environment")
    mask_tag_content("item > project", "key")

    # return root.prettify(encoding='utf-8')
    return str(root).encode("utf-8")


if __name__ == "__main__":
    import requests

    rs = requests.get(URL, headers=HEADERS, cert=PEM_FILE_NAME)
    print(rs)
    print(len(rs.text), repr(rs.text[:50]))

    # file_name = generate_file_name(URL)

    with open(FILE_NAME_FULL, mode="wb") as f:
        f.write(rs.content)

    with open(FILE_NAME, mode="wb") as f:
        f.write(clear_jira_xml(rs.content))
