#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/mozilla/bleach
# SOURCE: https://bleach.readthedocs.io/en/latest/linkify.html#preventing-links


# pip install bleach
from bleach.linkifier import Linker, build_url_re, build_email_re


# Preventing Links


def dont_linkify_python(attrs, new=False):
    # This is an existing link, so leave it be
    if not new:
        return attrs
    # If the TLD is '.py', make sure it starts with http: or https:.
    # Use _text because that's the original text
    link_text = attrs["_text"]
    if link_text.endswith(".py") and not link_text.startswith(("http:", "https:")):
        # This looks like a Python file, not a URL. Don't make a link.
        return None
    # Everything checks out, keep going to the next callback.
    return attrs


linker = Linker(callbacks=[dont_linkify_python])
print(linker.linkify("abc http://example.com def"))
# abc <a href="http://example.com">http://example.com</a> def

print(linker.linkify("abc models.py def"))
# abc models.py def

print("\n" + "-" * 100 + "\n")

linker = Linker(skip_tags=["pre"])
print(linker.linkify("a b c http://example.com d e f"))
# a b c <a href="http://example.com" rel="nofollow">http://example.com</a> d e f

print(linker.linkify("<pre>http://example.com</pre>"))
# <pre>http://example.com</pre>

print("\n" + "-" * 100 + "\n")

only_fish_tld_url_re = build_url_re(tlds=["fish"])
linker = Linker(url_re=only_fish_tld_url_re)

print(linker.linkify("com TLD does not link https://example.com"))
# com TLD does not link https://example.com

print(linker.linkify("fish TLD links https://example.fish"))
# fish TLD links <a href="https://example.fish" rel="nofollow">https://example.fish</a>

print("\n" + "-" * 100 + "\n")

only_https_url_re = build_url_re(protocols=["https"])
linker = Linker(url_re=only_https_url_re)

print(linker.linkify("gopher does not link gopher://example.link"))
# gopher does not link gopher://example.link

print(linker.linkify("https links https://example.com/"))
# https links <a href="https://example.com/" rel="nofollow">https://example.com/</a>

print("\n" + "-" * 100 + "\n")

html = "https://xn--80aaksdi3bpu.xn--p1ai/ https://дайтрафик.рф/"

linker = Linker(url_re=build_url_re(tlds=["рф"]))
print(linker.linkify(html))
# https://xn--80aaksdi3bpu.xn--p1ai/ <a href="https://дайтрафик.рф/" rel="nofollow">https://дайтрафик.рф/</a>

puny_linker = Linker(url_re=build_url_re(tlds=["рф", "xn--p1ai"]))
print(puny_linker.linkify(html))
# <a href="https://xn--80aaksdi3bpu.xn--p1ai/" rel="nofollow">https://xn--80aaksdi3bpu.xn--p1ai/</a> <a href="https://дайтрафик.рф/" rel="nofollow">https://дайтрафик.рф/</a>

print("\n" + "-" * 100 + "\n")

only_fish_tld_url_re = build_email_re(tlds=["fish"])
linker = Linker(email_re=only_fish_tld_url_re, parse_email=True)

print(linker.linkify("does not link email: foo@example.com"))
# does not link email: foo@example.com

print(linker.linkify("links email foo@example.fish"))
# links email <a href="mailto:foo@example.fish">foo@example.fish</a>
