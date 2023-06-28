import random
from re import findall

import requests

# rootVIII
# pycodestyle validated
# 2018-2020

# SOURCE: https://github.com/rootVIII/proxy_requests/blob/c8a4ebce4a9b9774b4cf7baa605dce3bbf879832/proxy_requests.py
# gil9red
# 2020-2023


DEBUG_LOG = False


class ProxyRequests:
    EXPECTED_ERRORS = [
        "ConnectTimeout",
        "ProxyError",
        "SSLError",
        "ReadTimeout",
        "ConnectionError",
        "ConnectTimeoutError",
    ]
    EMPTY_WARN = "Proxy Pool has been emptied"

    def __init__(self, url: str, timeout=5):
        self.url = url
        self.proxies = []
        self.used_proxy = None
        self.timeout = timeout
        self._acquire_sockets()

    def _acquire_sockets(self):
        rs = requests.get("https://www.sslproxies.org/")
        matches = findall(r"<td>\d+\.\d+\.\d+\.\d+</td><td>\d+</td>", rs.text)
        revised = [m.replace("<td>", "") for m in matches]
        self.proxies = [s[:-5].replace("</td>", ":") for s in revised]
        random.shuffle(self.proxies)

        DEBUG_LOG and print(f"[+] Total proxies: {len(self.proxies)}")

    def _pop_random_proxy(self) -> str:
        if not self.proxies:
            raise Exception(self.EMPTY_WARN)

        return self.proxies.pop()

    def _is_err(self, err):
        if type(err).__name__ not in self.EXPECTED_ERRORS:
            raise err

    def request(self, method: str, **kwargs) -> requests.Response:
        i = 0

        while True:
            i += 1

            current_proxy = self._pop_random_proxy()
            proxies = {
                "http": "http://" + current_proxy,
                "https": "https://" + current_proxy,
            }
            self.used_proxy = current_proxy

            try:
                DEBUG_LOG and print(f"[+] Attempt #{i}, proxy: {current_proxy}")

                rs = requests.request(
                    method,
                    self.url,
                    proxies=proxies,
                    timeout=self.timeout,
                    **kwargs,
                )

                return rs

            except Exception as e:
                DEBUG_LOG and print(
                    f"[#] Fail with {type(e).__name__}! Attempt #{i}, proxy: {current_proxy}"
                )
                self._is_err(e)

    def get(self, params=None, **kwargs) -> requests.Response:
        return self.request("get", params=params, **kwargs)

    def post(self, params=None, **kwargs) -> requests.Response:
        return self.request("post", params=params, **kwargs)

    def options(self, params=None, **kwargs) -> requests.Response:
        return self.request("options", params=params, **kwargs)

    def head(self, params=None, **kwargs) -> requests.Response:
        return self.request("head", params=params, **kwargs)

    def put(self, params=None, **kwargs) -> requests.Response:
        return self.request("put", params=params, **kwargs)

    def patch(self, params=None, **kwargs) -> requests.Response:
        return self.request("patch", params=params, **kwargs)

    def delete(self, params=None, **kwargs) -> requests.Response:
        return self.request("delete", params=params, **kwargs)
