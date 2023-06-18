#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


text_import = """
import datetime as DT
import sqlite3
from typing import List, Union
from pathlib import Path
import os
"""

print("\n".join(sorted(text_import.strip().splitlines(), key=lambda x: x.split()[1])))
# import datetime as DT
# import os
# from pathlib import Path
# import sqlite3
# from typing import List, Union
