from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
Mouse interaction

This piece of code will capture mouse clicks by the user. Every time the user
presses the left mouse the current point is pushed onto an array, when the right
mouse button is pressed the last element is removed from the array. After a click
a glutPostRedisplay() is called to trigger a call to the display function which
creates a line strip out of all created points.


http://www.de-brauwer.be/wiki/wikka.php?wakka=PyOpenGLMouse
"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


points = []


def initFun():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 640.0, 0.0, 480.0)


def displayFun():
    global points
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 0)
    for p in points:
        glVertex2i(p.x, p.y)
    glEnd()
    glFlush()


def mouseFun(button, state, x, y):
    global points
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        p = Point(x, 480 - y)
        points.append(p)
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if points:
            points = points[:-1]
    glutPostRedisplay()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"Polyline")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutMouseFunc(mouseFun)
    initFun()
    glutMainLoop()
