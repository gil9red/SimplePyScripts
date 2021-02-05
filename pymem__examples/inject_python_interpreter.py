#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pymem import Pymem
import os
import subprocess

notepad = subprocess.Popen(['notepad.exe'])

pm = Pymem('notepad.exe')
pm.inject_python_interpreter()
filepath = os.path.join(os.path.abspath('.'), 'pymem_injection.txt')
filepath = filepath.replace("\\", "\\\\")
shellcode = """
f = open("{}", "w+")
f.write("pymem_injection")
f.close()
""".format(filepath)
pm.inject_python_shellcode(shellcode)
notepad.kill()
