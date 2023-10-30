#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install PyYAML
import yaml


data = yaml.safe_load(
    """
__base_server: &__base_server
  title: "base_server"
  description: null
  ip: "127.0.0.1"
  ports:
    - 80
    - 8080

server_1:
  <<: *__base_server
  ip: "localhost"
  description: |
    Server running on <a href="http://localhost:80">address</a>
    
    <a href="http://localhost:80/about.html">See about</a>

server_2:
  <<: *__base_server
  ip: "localhost"
  ports: [123]
    """
)

import json
print(json.dumps(data, indent=4))
"""
{
    "__base_server": {
        "title": "base_server",
        "description": null,
        "ip": "127.0.0.1",
        "ports": [
            80,
            8080
        ]
    },
    "server_1": {
        "title": "base_server",
        "description": "Server running on <a href=\"http://localhost:80\">address</a>\n\n<a href=\"http://localhost:80/about.html\">See about</a>\n",
        "ip": "localhost",
        "ports": [
            80,
            8080
        ]
    },
    "server_2": {
        "title": "base_server",
        "description": null,
        "ip": "localhost",
        "ports": [
            123
        ]
    }
}
"""