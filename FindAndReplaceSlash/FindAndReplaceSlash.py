# -*- encoding: utf-8 -*-

# TODO: исправить способ замены
# TODO: вывод справки
# TODO: результаты:
##            сколько всего файлов
##            сколько в них было найдено
##            сколько всего файлов, в которых была замена

import re

__author__ = "ipetrash"

# Поиск в путях слешей вида \\, \ и // и замена на /
def updateFile( path ):
    print(u'\nFile: %s.' % path)
    f = open(path, 'r')
    text = f.read()

    p = re.compile(r'\.\.(.+(\\\\|\\|//))+(.*\.[\w]+)')
    iterator = p.finditer(text)
    for match in iterator:
        oldStr = match.group()        
        oldPos = match.span()
        
        ps = re.compile(r'\\\\|\\|//') # поиск слешей
        newStr = ps.sub(r'/', oldStr) # замена на /
        
        print('Found: "%s"%s --> %s' % (oldStr, oldPos, newStr))
        text = text.replace(oldStr, newStr) # произведем замену в тексте

    f = open(path, 'w')
    f.write(text)
        
    return ''

import os
import sys

if __name__ == "__main__":
    # @type pathDir str
    # @type suffix str
    argv = sys.argv
    if (len(argv) > 2):
        pathDir = argv[1]
        suffix = argv[2]
        print(u'Directory: %s' % pathDir)

        for dirname, dirnames, filenames in os.walk(pathDir):
            # Выведем пути до всех файлов.
            for filename in filenames:
                if filename.endswith(suffix):
                    updateFile(os.path.join(dirname, filename))
