__author__ = 'ipetrash'


import feedparser
# import HTMLParser

if __name__ == '__main__':
    d = feedparser.parse('http://bash.im/rss/')
    # print(d["feed"]["subtitle"])
    #
    # for entry in d["entries"]:
    #     quote = entry["summary"]
    #     h = HTMLParser.HTMLParser()
    #     quote = h.unescape(quote).replace("<br />", "\n")
    #     print(quote + '\n\n')

    print(d.feed.subtitle)

    for entry in d.entries:
        quote = entry.summary
        # h = HTMLParser.HTMLParser()
        # quote = h.unescape(quote).replace("<br />", "\n")
        print(quote + '\n\n')
