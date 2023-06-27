#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import subprocess

from subprocess import Popen, PIPE, STDOUT


WIN_DIR = os.path.expandvars("%WINDIR%")
FILE_NAME_POWERSHELL = os.path.join(
    WIN_DIR, r"system32\WindowsPowerShell\v1.0\powershell.exe"
)
print("Powershell:", FILE_NAME_POWERSHELL)
print()

file_name_ps1 = "hello_world.ps1"
command = FILE_NAME_POWERSHELL + " -ExecutionPolicy Bypass -File " + file_name_ps1

print("OS:")
os.system(command)

print()

print("subprocess.call:")
retcode = subprocess.call(command, stderr=subprocess.STDOUT)
print(retcode)

print()
print("subprocess.check_output:")
output = subprocess.check_output(
    command, universal_newlines=True, stderr=subprocess.STDOUT
)
print(output)

print()
print("subprocess.run:")
rs = subprocess.run(command)
print(rs.returncode)

print()
print("subprocess.Popen:")

rs = Popen(command, universal_newlines=True, stdout=PIPE, stderr=STDOUT)
for line in rs.stdout:
    line = line.rstrip()
    print(line)
