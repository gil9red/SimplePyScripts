#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket
import ssl

from urllib.parse import urlsplit


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = "https://www.coursera.org/robots.txt"

result = urlsplit(url)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s_sock = context.wrap_socket(socket, server_hostname=result.netloc)
s_sock.connect((result.netloc, 443))

cmd = f"GET {result.path} HTTP/1.1\r\nHost: {result.netloc}\r\n\r\n".encode()
s_sock.send(cmd)

while True:
    data = s_sock.recv(512)
    if not data:
        break

    print(data.decode(), end="")

s_sock.close()

# HTTP/1.1 200 OK
# Content-Type: text/plain
# Content-Length: 641
# Connection: keep-alive
# Accept-Ranges: bytes
# Access-Control-Allow-Methods: GET
# Access-Control-Allow-Origin: *
# Cache-Control: private, no-cache, no-store, must-revalidate, max-age=0
# Date: Mon, 30 Mar 2020 10:26:21 GMT
# ETag: "810792ef38d0270d49dc00a9405e7c15"
# Last-Modified: Fri, 04 Oct 2019 17:28:21 GMT
# Server: AmazonS3
# Set-Cookie: CSRF3-Token=1586427980.PE8pbeuhTZIhyPdx; Max-Age=864000; Expires=Thu, 09 Apr 2020 10:26:20 GMT; Path=/; Domain=.coursera.org
# Set-Cookie: __204u=4520938868-1585563980368; Max-Age=31536000; Expires=Tue, 30 Mar 2021 10:26:20 GMT; Path=/; Domain=.coursera.org
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# Vary: Origin
# x-amz-version-id: null
# X-Content-Type-Options: nosniff
# X-Coursera-Request-Id: 5bButHJwEeq41wq5SIXE2w
# X-Coursera-Trace-Id-Hex: 651682df3db76569
# X-Frame-Options: SAMEORIGIN
# X-XSS-Protection: 1; mode=block
# X-Cache: Miss from cloudfront
# Via: 1.1 cf9168a8e884185dcf2dfe5f17902ab1.cloudfront.net (CloudFront)
# X-Amz-Cf-Pop: ARN53
# X-Amz-Cf-Id: EftP8CvSi31vRpoS2b_9PARQVld18x1_tURlTtUDKnsNo2Z5_fqASA==
#
# User-agent: *
# Allow: /api/utilities/v1/imageproxy
# Disallow: /maestro/api/
# Disallow: /api/
# Disallow: /maestro/
# Disallow: /ui/
# Disallow: /signature/voucher/
# Disallow: /account/email_verify/
# Disallow: /acclaimbadge/
# Disallow: /voucher/
# Disallow: /search
# Disallow: /learn-perf/
# Disallow: /specializations-perf/
# Disallow: /professional-certificates-perf/
# Disallow: /learn-noperf/
# Disallow: /specializations-noperf/
# Disallow: /professional-certificates-noperf/
# Disallow: /business/xmlrpc.php
# Disallow: /business/wp-content/uploads/
# Sitemap: https://www.coursera.org/sitemap.xml
# Sitemap: https://www.coursera.org/coursera-for-business-sitemap.xml
