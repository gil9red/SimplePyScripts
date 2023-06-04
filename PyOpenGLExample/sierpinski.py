import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
Sierpinski's triangle.

Sierpinski's triangle∞ is an image which has always fascinated me. The technique
used here is the so called Chaos game∞ here we generate a constellation of points
which ends up being Sierpinski's triangle. The algorithm is as follows:
Pick three points which form the outer boundaries of the triangle
Pick a midpoint of one of the lines which make up an edge
Until we're happy with the amount of detail a new dot is formed by the midpoint of
the current midpoint and one of the three points of the triangle

http://en.wikipedia.org/wiki/Sierpinski_triangle
http://en.wikipedia.org/wiki/Chaos_game
"""


def initFun():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 640.0, 0.0, 480.0)


def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    x = [0.0, 640.0, 320.0]
    y = [0.0, 0.0, 480.0]

    curx = 0
    cury = 320
    glVertex2f(curx, cury)
    for i in range(0, 500000):
        idx = random.randint(0, 2)
        curx = (curx + x[idx]) / 2.0
        cury = (cury + y[idx]) / 2.0
        glVertex2f(curx, cury)
    glEnd()
    glFlush()


if __name__ == "__main__":
    # This is the current implementation, note that all points are recalculated on
    # a window update, for any other purpose than showing off with how simply it is
    # to create this eyecode you'd probably want to precalculate the dots and put them
    # in a display list.

    glutInit()
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Sierpinski")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()
