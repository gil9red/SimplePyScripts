from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
A hello world application

This pages creates a simple window to which 2d orthogonal projection is applied.
Next a couple of points are drawn. This will create a white window with three black
dots.

url = http://www.de-brauwer.be/wiki/wikka.php?wakka=PyOpenGLHelloWorld
"""


def initFun() -> None:
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(4.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 640.0, 0.0, 480.0)


def displayFun() -> None:
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    glVertex2i(100, 50)
    glVertex2i(100, 130)
    glVertex2i(150, 130)
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Drawdots")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()
