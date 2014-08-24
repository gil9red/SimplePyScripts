__author__ = 'ipetrash'

import base64
import sys

if __name__ == '__main__':
    text = input("Text: ")
    if not text:
        print("Empty text!")
        sys.exit(1)

    print("Result:")
    print("  base16: %s" % base64.b16encode(text.encode()).decode())
    print("  base32: %s" % base64.b32encode(text.encode()).decode())
    print("  base64: %s" % base64.b64encode(text.encode()).decode())
    print("  base85: %s" % base64.b85encode(text.encode()).decode())
    
    print()
    print(base64.b64decode("VFJBQ0sx").decode("utf8"))
    print(base64.b64decode("MTEyMg==").decode("utf8"))
    print(base64.b64decode("MzIx").decode("utf8"))
