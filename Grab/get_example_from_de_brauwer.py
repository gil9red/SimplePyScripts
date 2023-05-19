
__author__ = "ipetrash"


import re
import os

from grab import Grab


"""Пример получения исходного кода с сайта www.de-brauwer.be."""


def get_example_from_de_brauwer(wakka):
    g = Grab()
    g.go("http://www.de-brauwer.be/wiki/wikka.php?wakka=" + wakka)
    code_html = g.doc.select('//div[@class="code"]').html()

    pattern = r'(<div class="code".*?>)' "|</div.*?>" "|<span.*?>" "|</span.*?>" "|<br>"
    source_code = re.sub(pattern, "", code_html)
    source_code = re.sub("\xa0", " ", source_code)  # remove &nbsp;
    return source_code


DIR_NAME = "PyOpenGLExample"
os.makedirs(DIR_NAME, exist_ok=True)

examples = [
    "PyOpenGLHelloWorld",
    "PyOpenGLSierpinski",
    "PyOpenGLSquares",
    "PyOpenGLCheckerBoard",
    "PyOpenGLMouse",
    "PyOpenGLScatter",
    "PyOpenGLGingerbread",
    "PyOpenGLMaze",
    "PyOpenGLReshape",
    "PyOpenGLTurtle",
    "PyOpenGLRosette",
    "PyOpenGLWireframe",
]

for e in examples:
    source_code = get_example_from_de_brauwer(e)

    with open(os.path.join(DIR_NAME, e + ".py"), mode="w", encoding="utf-8") as f:
        f.write(source_code)
