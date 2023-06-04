import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
Turtle drawings

Once the functions reset(), turn(), turnTo() and forw() there is a possibility to
program a path. In essence this is very similar to using polar coordinates relative
to the last set point. Meaning you define the angle and the length over which a line
should be drawn. First an example will be given containing the full source, next will
will only focus on the display function since the same primitives will be used.


http://www.de-brauwer.be/wiki/wikka.php?wakka=PyOpenGLTurtle
"""

curX = 0.0
curY = 0.0
angle = 0.0


def reset():
    """Reset the position to the origin"""
    global curX
    global curY
    global angle

    curX = 0.0
    curY = 0.0
    angle = 0.0


def turnTo(deg):
    """Turn to a certain angle"""
    global angle
    angle = deg


def turn(deg):
    """Turn a certain number of degrees"""
    global angle
    angle += deg


def forw(len, visible):
    """Move forward over a certain distance"""
    global curX
    global curY
    tmpX = curX
    tmpY = curY
    curX = curX + len * math.cos(math.radians(angle))
    curY = curY + len * math.sin(math.radians(angle))
    if visible:
        glBegin(GL_LINE_STRIP)
        glVertex2f(tmpX, tmpY)
        glVertex2f(curX, curY)
        glEnd()


def initFun():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-100, 100, -100, 100)


def reshapeFun(w, h):
    glViewport(0, 0, w, h)
    # if w > h:
    # glViewport((w-h)/2,0,h,h)
    # else:
    # glViewport(0,(h-w)/2,w,w)


def turtle_1():
    glClear(GL_COLOR_BUFFER_BIT)
    reset()
    glColor3f(0.0, 0.0, 1.0)
    L = 30
    turnTo(0)
    for i in range(0, 4):
        forw(3 * L, True)
        turn(90)
        forw(L, True)
        turn(90)
        forw(L, True)
        turn(90)
    glFlush()


def turtle_2():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    length = 0
    increment = 1
    for i in range(0, 100):
        forw(length, True)
        turn(60)
        length += increment
    glFlush()


def turtle_3():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    length = 0
    increment = 1
    for i in range(0, 200):
        forw(length, True)
        turn(89.5)
        length += increment
    glFlush()


def turtle_4():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    length = 0
    increment = 1
    for i in range(0, 200):
        forw(length, True)
        turn(-144)
        length += increment
    glFlush()


def turtle_5():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    length = 0
    increment = 1
    for i in range(0, 200):
        forw(length, True)
        turn(170)
        length += increment
    glFlush()


def turtle_6():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    L = 10
    length = L
    for i in range(0, 10):
        for j in range(0, 4):
            forw(length, True)
            turn(90)
        length += L
    glFlush()


def turtle_7():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    L = 3
    length = L
    for i in range(0, 100):
        forw(length, True)
        turn(90)
        length += L
    glFlush()


def turtle_8():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    forw(100, True)
    turn(120)
    forw(100, True)
    turn(120)
    forw(50, True)
    turn(120)
    forw(50, True)
    turn(-120)
    forw(50, True)
    turn(-120)
    forw(50, True)
    turn(120)
    forw(50, True)
    glFlush()


def turtle_9():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    L = 50
    for i in range(0, 3):
        forw(L, True)
        turn(-60)
        forw(L, True)
        turn(-120)
        forw(L, True)
        turn(-60)
        forw(L, True)
    glFlush()


def turtle_10():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 1.0)
    reset()
    L = 30
    for i in range(0, 3):
        forw(L, True)
        turn(60)
        forw(L, True)
        turn(60)
        forw(L, True)
        turn(60)
        forw(L, True)
        turn(-60)

    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(400, 400)
    glutCreateWindow(b"Turtle")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    glutDisplayFunc(turtle_1)
    # glutDisplayFunc(turtle_2)
    # glutDisplayFunc(turtle_3)
    # glutDisplayFunc(turtle_4)
    # glutDisplayFunc(turtle_5)
    # glutDisplayFunc(turtle_6)
    # glutDisplayFunc(turtle_7)
    # glutDisplayFunc(turtle_8)
    # glutDisplayFunc(turtle_9)
    # glutDisplayFunc(turtle_10)

    glutReshapeFunc(reshapeFun)
    initFun()
    glutMainLoop()
