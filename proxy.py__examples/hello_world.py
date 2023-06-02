#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/abhinavsingh/proxy.py


import ipaddress

# pip install --upgrade proxy.py
import proxy
from proxy.common.utils import bytes_
from proxy.http.parser import HttpParser
from proxy.plugin import FilterByUpstreamHostPlugin
from proxy.http.proxy import HttpProxyBasePlugin


# NOTE: Analog https://github.com/gil9red/SimplePyScripts/blob/3d8afdec07c2cfbc94fcb3fd792721e1e8565a42/http.server__examples/simple_http_proxy_server/main.py#L18
class AddHeadersPlugin(HttpProxyBasePlugin):
    def before_upstream_connection(self, request: HttpParser) -> HttpParser | None:
        return request

    def handle_client_request(self, request: HttpParser) -> HttpParser | None:
        # NOTE: Add custom header
        request.add_header(b"x-my-proxy", b"hell yeah!")
        request.add_header(b"x-my-client-ip", bytes_(self.client.addr[0]))

        return request

    def handle_upstream_chunk(self, chunk: memoryview) -> memoryview:
        return chunk

    def on_upstream_connection_close(self) -> None:
        pass


def main(*args, **kwargs):
    proxy.main(
        *args,
        hostname=ipaddress.ip_address("127.0.0.1"),
        port=33333,
        plugins=[
            "proxy.plugin.CacheResponsesPlugin",  # Adding plugin v1
            FilterByUpstreamHostPlugin,  # Adding plugin v2
            AddHeadersPlugin,  # Adding custom plugin
        ],
        **kwargs
    )


if __name__ == "__main__":
    main()
