#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Riddle with a cipher from Might and Magic VII


from itertools import cycle
from string import ascii_uppercase


message = """\
Y iupj xckox nmw henv ik eoiuyl pwzmjh usv vqwy xjvisfx nmw qeey zwga xjm htlsi. 
Jn cx fchub yfkh iponm osiu uhi usduyl. Rq xec cm igbu bhx yzs tfvn uswt. Hiii disl.
""".upper()
secret = "PATTERN"

items = []

iter_secret = cycle(secret)

for c in message:
    if c in ascii_uppercase:
        k = next(iter_secret)
        c = ascii_uppercase[(ord(c) - ord(k) - 1) % 26]

    items.append(c)

print("".join(items))
# I HAVE FOUND THE TOMB OF MASTER KELWIN AND HAVE DEDUCED THE CODE FROM HIS NOTES.
# IT IS NORTH EAST SOUTH WEST AND CENTER. MY JOB IS DONE AND THE DEBT PAID. GOOD LUCK.
