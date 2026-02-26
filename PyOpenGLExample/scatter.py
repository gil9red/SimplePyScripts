import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
Creating a scatter plot of a pseudo random number generator

The goal is to create a scatter plot where a point is defined by the current output
of a pseudo random number generator (PRNG) and the next output of the PRNG. The idea
is that a low quality PRNG will show clusters and that ways make predicting the next
result of the pseudo random generator easy. A practical application of this is the
prediction of TCP sequence numbers (see this page∞ for more information.


http://www.de-brauwer.be/wiki/wikka.php?wakka=PyOpenGLScatter
"""


def initFun() -> None:
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 400.0, 0.0, 400.0)


def getRandom(mode):
    """
    Wrapper around several RNG's. If mode is 0 random.randint() is used, if
    mode is one a guassian distribution is used.
    """
    if mode == 0:
        return random.randint(0, 400)
    elif mode == 1:
        return random.gauss(200, 40) % 400


def displayFun() -> None:
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    randMode = 1
    a = getRandom(randMode)
    b = getRandom(randMode)
    for i in range(0, 500000):
        glVertex2f(a, b)
        a = b
        b = getRandom(randMode)
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(400, 400)
    glutCreateWindow(b"Scatter")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()
