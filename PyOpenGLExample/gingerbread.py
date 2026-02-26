from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
The gingerbread man

The gingerbread man is again iterated function sequence ( see mathworld.wolfram.com∞
for example). This code generates the gingerbread man based on the parameters
suggested in the book. But the starting point can be altered by clicking the mouse.


http://www.de-brauwer.be/wiki/wikka.php?wakka=PyOpenGLGingerbread
"""

x = 115
y = 121


def initFun() -> None:
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(4.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 640.0, 0.0, 480.0)


def mouseFun(button, state, xIn, yIn) -> None:
    global x
    global y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x = xIn
        y = 480 - yIn

    glutPostRedisplay()


def displayFun() -> None:
    global x
    global y
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    M = 40
    L = 3
    for i in range(0, 500000):
        glVertex2f(x, y)
        tmp = x
        x = M * (1 + 2 * L) - y + abs(x - L * M)
        y = tmp
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Gingerbread")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutMouseFunc(mouseFun)
    initFun()
    glutMainLoop()
