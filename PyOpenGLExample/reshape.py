from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
Handling window reshape and the aspect ratio

In the 2D world we're living in, gluOrtho2D is used to map the window to certain
coordinates, however reshaping the window might still result in an odd looking aspect
ratio. For this purpose a callback function for the reshape event is created which
will map the coordinates mapped with gluOrtho2D to a square viewport (and hence limit
the drawable region on the screen), this while maintaining an aspect ratio of one
(making a square look like a square and not like a rectangle). The following example
will display a teapot in blue and it will show the edge of the viewport in red, this
while keeping the center of the viewport, the center of the screen. The glViewport
function takes the lower left corner x and y and the width and height of the viewport
as arguments.
"""


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
    glutWireTeapot(40)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINE_STRIP)
    glVertex2f(-99, -99)
    glVertex2f(-99, 99)
    glVertex2f(99, 99)
    glVertex2f(99, -99)
    glVertex2f(-99, -99)
    glEnd()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Viewport")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(display_fun)
    glutReshapeFunc(reshape_fun)
    init_fun()
    glutMainLoop()
