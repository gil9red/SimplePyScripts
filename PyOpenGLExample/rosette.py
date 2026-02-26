import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
Rosette

Introduction
A rosette appears when the points of an n-gon (regular polygon with points
P_i = (R cos(2*pi*i/n),R sin(2*pi*i/n)) ) are connected to all other points of
the n-gon. E.g. when n=5, the result is an outer pentagon and an inner pentagram.
In the code below, first all points of the n-gon are calculated, then a double for
loop connect points i to points i+1,...,n-1,n.


http://www.de-brauwer.be/wiki/wikka.php?wakka=PyOpenGLRosette
"""

N = 25
RADIUS = 95


def init_fun() -> None:
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-100, 100, -100, 100)


def reshape_fun(w, h) -> None:
    glViewport(0, 0, w, h)

    # if w > h:
    # glViewport((w - h) / 2, 0, h, h)
    # else:
    #     glViewport(0, (h - w) / 2, w, w)


def display_fun() -> None:
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    xpts = []
    ypts = []
    for i in range(0, N):
        xpts.append(RADIUS * math.sin(2.0 * math.pi * i / N))
        ypts.append(RADIUS * math.cos(2.0 * math.pi * i / N))

    glBegin(GL_LINE_STRIP)
    for i in range(0, N):
        for j in range(i, N):
            glVertex2f(xpts[i], ypts[i])
            glVertex2f(xpts[j], ypts[j])
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(400, 400)
    glutCreateWindow(b"Rosette")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(display_fun)
    glutReshapeFunc(reshape_fun)
    init_fun()
    glutMainLoop()
